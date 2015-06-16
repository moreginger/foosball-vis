#!/usr/bin/env python

import urllib2
import re
import datetime
import json
from shapely.geometry import LineString
from games import Game, games

__epoch__ = datetime.datetime(1970, 1, 1)
__days_lookahead__ = 60
day_seconds = 24 * 60 * 60


class Ranking:

    def __init__(self, time, ranking):
        self.time = time
        self.ranking = ranking

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '%s:%s' % (self.time, self.ranking)


class Player:

    def __init__(self, name, lead_in_seconds):
        self.name = name
        self.lead_in_seconds = lead_in_seconds
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
        ranking_changed = self.rankings and self.rankings[-1] and self.rankings[-1].ranking != ranking
        if ranking_changed:
            # Extra data point for pretty lines up/down
            extra_ranking = Ranking(time - self.lead_in_seconds, self.rankings[-1].ranking)
            popped = None
            if self.rankings and self.rankings[-1] and self.rankings[-1].time > extra_ranking.time and self.rankings[-1].ranking != ranking:
                popped = self.rankings.pop(-1)

                if not self.rankings or not self.rankings[-1]:
                    # Popped the last point
                    # First approximation: put it back
                    # TODO: Move the line back according to imagined projection back?
                    extra_ranking = popped
                else:
                    # There is a previous point, intersect lines
                    previous = self.rankings[-1]
                    line1 = LineString([(previous.time, previous.ranking), (popped.time, popped.ranking)])
                    line2 = LineString([(extra_ranking.time + (extra_ranking.time - time), extra_ranking.ranking + (extra_ranking.ranking - ranking)), (time, ranking)])
                    geom = line1.intersection(line2)
                    # TODO improve test!
                    extra_ranking = Ranking(geom.x, geom.y) if geom.geom_type is 'Point' else None

            if extra_ranking:
                self.rankings.append(extra_ranking)

        if ranking_changed or inactivate or not self.rankings or not self.rankings[-1]:
            self.rankings.append(Ranking(time, ranking))

        if inactivate:
            self.active = False
            self.rankings.append(None)

    def write_final_rank(self, time):
        if self.active and self.rankings[-1]:
            self.rankings.append(Ranking(time, self.rankings[-1].ranking))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.name


class Analysis:

    def __init__(self, importance = 25, retire_days = 60, lead_in_seconds = 16 * 60 * 60, teams = {}):
        self.importance = importance
        self.retire_days = retire_days
        self.lead_in_seconds = lead_in_seconds
        self.player_to_team = dict((v, k) for k in teams for v in teams[k])
        self.players = {}
        self.games = []

    def get_player(self, name):
        if self.player_to_team: 
            name = self.player_to_team[name] if name in self.player_to_team else 'other'
        if name in self.players:
            return self.players[name]
        else:
            player = self.players[name] = Player(name, self.lead_in_seconds)
            return player

    def game_played(self, new_game):
        self.process_games(time = new_game.time)

        self.games.append(new_game)
        self.get_player(new_game.blue_player).most_recent_game = new_game.time
        self.get_player(new_game.red_player).most_recent_game = new_game.time

    def process_games(self, time=None, flush=False):
        while self.games and (flush or time - self.games[0].time >= self.retire_days * day_seconds):
            game = self.games.pop(0)
            blue = self.get_player(game.blue_player)
            red = self.get_player(game.red_player)

            predict = 1 / (1 + 10 ** ((red.elo - blue.elo) / 180))
            result = game.blue_score / (game.blue_score + game.red_score)
            delta = self.importance * (result - predict)

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
                player.write_final_rank((datetime.datetime.now() - __epoch__).total_seconds())


class RankingsEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Player):
            return {'label': obj.name, 'elo': '{0:.3f}'.format(obj.elo), 'data': obj.rankings}
        if isinstance(obj, Ranking):
            return [obj.time * 1000, obj.ranking]
        else:
            return super(FootballJsonEncoder, self).default(obj)


def main(analysis_kwargs):
    analysis = Analysis(**analysis_kwargs)
    for game in games():
        analysis.game_played(game)

    analysis.process_games(flush = True)

    print("Content-type: application/json\n")
    print(RankingsEncoder().encode(analysis.players.values()))


if __name__ == '__main__':
    main({})
