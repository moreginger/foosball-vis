#!/usr/bin/env python

import urllib2
import re
import datetime
import json
from random import shuffle
import games
from collections import Counter


def main():
    print("Content-type: application/json\n")

    games_by_player = Counter()
    def game_data(g):
        blue = g.blue_player
        red = g.red_player
        games_by_player[blue] += 1
        games_by_player[red] += 1
        return {'time': g.time, 'blue': { 'name' : blue, 'score': g.blue_score, 'game': games_by_player[blue] }, 'red': { 'name': g.red_player, 'score': g.red_score, 'game': games_by_player[red] } }

    data = [game_data(x) for x in games.games()][-5000:]
    shuffle(data)
    players = set([name for sublist in [[g['red']['name'], g['blue']['name']] for g in data] for name in sublist])
    players = [{'name': p, 'games': games_by_player[p]} for p in players]
    print(json.JSONEncoder().encode({'games': data, 'players': players}))


if __name__ == '__main__':
    main()
