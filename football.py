import urllib2
import re
import datetime

__epoch__ = datetime.datetime(1970, 1, 1)
__days_lookahead__ = 60

class Game:

    def __init__(self, time, blue_player, blue_score, red_player, red_score):
        self.time = time
        self.blue_player = blue_player
        self.blue_score = blue_score
        self.red_player = red_player
        self.red_score = red_score

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        timestamp = int((self.time - __epoch__).total_seconds())
        return '{time} {red} v {blue}'.format(time=timestamp, red=self.red_player, blue=self.blue_player)


def games():
    r = re.compile(r'(.+) ([0-9]+) (.+) ([0-9]+) ([0-9]+)')
    data = urllib2.urlopen('http://int.corefiling.com/~aks/football/ladder.txt')
    # data = open('ladder.txt')
    for line in data:
        m = r.match(line)
        if m:
            d = datetime.datetime.fromtimestamp(int(m.group(5)))
            yield Game(d, m.group(1).lower(), float(m.group(2)), m.group(3).lower(), float(m.group(4)))


class Player:

    def __init__(self, name):
        self.name = name
        self.elo = 0.0
        self.games = 0
        self.most_recent_game = None
        self.active = False
        self.rankings = []

    def game(self, delta, time):
        self.active = True
        self.elo += delta
        self.games += 1

    def update_ranking(self, ranking, time, inactivate=False):
        ranking_changed = self.rankings and (not self.rankings[-1] or self.rankings[-1][0] != ranking)
        if ranking_changed and self.rankings[-1]:
            # Extra data point for nice lines up/down
            extra_time = time - datetime.timedelta(1)
            extra_ranking = self.rankings[-1][0]
            popped = None
            while self.rankings and self.rankings[-1] and self.rankings[-1][1] > extra_time and self.rankings[-1][0] != ranking:
                popped = self.rankings.pop(-1)

            if popped and self.rankings and self.rankings[-1]:
                previous = self.rankings[-1]
                interval = time - previous[1]
                extra_time = interval / 2 + previous[1]
                fraction = float(interval.total_seconds()) / 24 / 60 / 60 / 2
                extra_ranking = fraction * (popped[0] - previous[0]) + previous[0]

            if self.rankings and self.rankings[-1]:
                self.rankings.append((extra_ranking, extra_time))

        if not self.rankings or inactivate or ranking_changed:
            self.rankings.append((ranking, time))

        if inactivate:
            self.active = False
            self.rankings.append(())

    def write_final_rank(self, time):
        if self.active and self.rankings[-1]:
            self.rankings.append((self.rankings[-1][0], time))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.name


class Analysis:

    def __init__(self):
        self.players = {}
        self.games = []

    def get_player(self, name):
        if name in self.players:
            return self.players[name]
        else:
            player = self.players[name] = Player(name)
            return player

    def game_played(self, new_game):

        if '-' in new_game.blue_player or '-' in new_game.red_player:
            # Filter out pdw-right etc.
            return

        self.process_games(time = new_game.time)

        self.games.append(new_game)
        self.get_player(new_game.blue_player).most_recent_game = new_game.time
        self.get_player(new_game.red_player).most_recent_game = new_game.time

    def process_games(self, time=None, flush=False):
        game = None
        while self.games and (flush or (time - self.games[0].time).days >= __days_lookahead__):
            game = self.games.pop(0)
            blue = self.get_player(game.blue_player)
            red = self.get_player(game.red_player)

            predict = 1 / (1 + 10 ** ((red.elo - blue.elo) / 180))
            result = game.blue_score / (game.blue_score + game.red_score)
            delta = 25 * (result - predict)

            blue.game(delta, game.time)
            red.game(-delta, game.time)

            players_by_rank = sorted([p for p in self.players.values() if p.active], key=lambda x: x.elo, reverse=True)

            rank = 1
            for player in players_by_rank:
                inactivate = not flush and player.most_recent_game == game.time
                player.update_ranking(rank, game.time, inactivate=inactivate)
                rank += 1

        if flush:
            for player in self.players.values():
                player.write_final_rank(game.time)


def main():
    analysis = Analysis()
    for game in games():
        analysis.game_played(game)

    analysis.process_games(flush = True)

    # TODO use remaining values
    dataset_tmpl = '{{label: "{name}", data: [{data}]}}'
    datasets = [
        dataset_tmpl.format(
            name=p.name,
            data=','.join(['[{time},{elo}]'.format(time=(r[1] - __epoch__).total_seconds() * 1000, elo=r[0]) if r else 'null' for r in p.rankings])
        ) for p in analysis.players.values()
    ]
    datasets_tmpl = 'var data = [{data}];'

    with open('data.js', 'w') as f:
        f.write(datasets_tmpl.format(data = ','.join(datasets)))


if __name__ == '__main__':
    main()
