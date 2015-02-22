import urllib2
import re
import datetime


class Game:
    def __init__(self, time, blue_player, blue_score, red_player, red_score):
        self.time = time
        self.blue_player = blue_player
        self.blue_score = blue_score
        self.red_player = red_player
        self.red_score = red_score


def games():
    r = re.compile(r'(.+) ([0-9]+) (.+) ([0-9]+) ([0-9]+)')
    # data = urllib2.urlopen('http://int.corefiling.com/~aks/football/ladder.txt')
    data = open('ladderShort.txt')
    for line in data:
        m = r.match(line)
        if m:
            d = datetime.datetime.fromtimestamp(int(m.group(5)))
            yield Game(d, m.group(1), float(m.group(2)), m.group(3), float(m.group(4)))


class Player:

    def __init__(self, name):
        self.name = name
        self.elo = 0.0
        self.games = 0
        self.last_game = None
        self.rankings = []

    def game(self, delta, time):
        self.elo += delta
        self.games += 1
        self.last_game = time

    def update_ranking(self, ranking, time):
        if not self.rankings or self.rankings[-1][0] != ranking:
            self.rankings.append((ranking, time))
        if (time - self.last_game).days > 60:
            # Break continuity.
            while self.rankings[-1][1] > self.last_game:
                self.rankings.pop(-1)
            # TODO: What if their last game didn't cause a ranking change. Need to add a value here.
            self.rankings.append(())


class Analysis:

    def __init__(self):
        self.players = {}

    def get_player(self, name):
        if name in self.players:
            return self.players[name]
        else:
            player = self.players[name] = Player(name)
            return player

    def game_played(self, game):
        if '-' in game.blue_player or '-' in game.red_player:
            # Filter out pdw-right etc.
            return

        blue = self.get_player(game.blue_player)
        red = self.get_player(game.red_player)
        predict = 1 / (1 + 10 ** ((red.elo - blue.elo) / 180))
        result = game.blue_score / (game.blue_score + game.red_score)
        delta = 25 * (result - predict)

        blue.game(delta, game.time)
        red.game(-delta, game.time)

        players_by_rank = sorted([p for p in self.players.values()], key=lambda x: x.elo)
        rank = 1
        for player in players_by_rank:
            player.update_ranking(rank, game.time)
            rank += 1


def main():
    analysis = Analysis()
    for game in games():
        analysis.game_played(game)

    # TODO use remaining values
    dataset_tmpl = '{{label: "{name}", data: [{data}]}}'
    epoch = datetime.datetime(1970, 1, 1)
    datasets = [
        dataset_tmpl.format(
            name=p.name,
            data=','.join(['[{time},{elo}]'.format(time=(r[1] - epoch).total_seconds(), elo=r[0]) for r in p.rankings])
        ) for p in analysis.players.values()
    ]
    datasets_tmpl = 'var datasets = [{datasets}];'

    with open('datasets.js', 'w') as f:
        f.write(datasets_tmpl.format(datasets = ','.join(datasets)))

    for k, v in analysis.players.iteritems():
        print (k, v.elo)


if __name__ == '__main__':
    main()
