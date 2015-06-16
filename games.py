#!/usr/bin/env python

import re


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
        return '{time} {red} v {blue}'.format(time=self.time, red=self.red_player, blue=self.blue_player)


def games():
    # Don't permit $player-right and such variations... they don't represent true skill of player.
    r = re.compile(r'^\s*([^\s-]+)\s+([0-9]+)\s+([^\s-]+)\s+([0-9]+)\s+([0-9]+)\s*$')
    data = open('ladder.txt')
    for line in data:
        m = r.match(line)
        if m:
            yield Game(int(m.group(5)), m.group(1).lower(), float(m.group(2)), m.group(3).lower(), float(m.group(4)))
