import urllib2
import re
from collections import defaultdict

class Game:
    def __init__(self, time, blue_player, blue_score, red_player, red_score):
        self.time = time
        self.blue_player = blue_player
        self.blue_score = blue_score
        self.red_player = red_player
        self.red_score = red_score


def games():
    r = re.compile(r'(.+) ([0-9]+) (.+) ([0-9]+) ([0-9]+)')
    data = urllib2.urlopen('http://int.corefiling.com/~aks/football/ladder.txt')
    for line in data:
        m = r.match(line)
        if m:
            yield Game(int(m.group(5)), m.group(1), float(m.group(2)), m.group(3), float(m.group(4)))


class Player:

    def __init__(self):
        self.elo = 0.0
        self.games = 0

    def game(self, delta):
        self.elo += delta
        self.games += 1

    def is_ranking(self):
        return self.games >= 10


class Analysis:

    def __init__(self):
        self.rankings = []
        self.players = defaultdict(Player)

    def game_played(self, game):
        blue = self.players[game.blue_player]
        red = self.players[game.red_player]
        predict = 1 / (1 + 10 ** ((red.elo - blue.elo) / 180))
        result = game.blue_score / (game.blue_score + game.red_score)
        delta = 25 * (result - predict)

        left.game(delta)
        right.game(-delta)
        self.rankings += [(game.time, sorted([p for p in players.keys()], key=lambda x: x.elo))]


def main():
    analysis = Analysis()
    for game in games():
        analysis.game_played(blue, red, delta)

    for k, v in analysis.players.iteritems():
        print (k, v.elo)


if __name__ == '__main__':
    main()
