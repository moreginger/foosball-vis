#!/usr/bin/env python

import urllib2
import re
import datetime
import json
from games import Game, games

class GamesEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Game):
            return {'time' : obj.time, 'blue': { 'name' : obj.blue_player, 'score': obj.blue_score }, 'red': { 'name': obj.red_player, 'score': obj.red_score } }


def main():
    print("Content-type: application/json\n")
    print(GamesEncoder().encode(list(reversed(list(games())[-1000:]))))


if __name__ == '__main__':
    main()
