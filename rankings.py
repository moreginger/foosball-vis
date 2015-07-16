#!/usr/bin/env python

import urllib2
import re
import datetime
import json
from collections import defaultdict
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

    def __init__(self, name, retire_seconds, lead_in_seconds):
        self.name = name
        self.retire_seconds = retire_seconds
        self.lead_in_seconds = lead_in_seconds
        self.elo = 0.0
        self.most_recent_game = None
        self.rankings = []

    def game(self, delta, time):
        self.elo += delta
        self.most_recent_game = time

    def is_active(self, time):
        return time - self.most_recent_game < self.retire_seconds

    def is_retired(self):
        return self.rankings[-1].ranking == -1

    def update_ranking(self, ranking):
        ranking_changed = self.rankings and self.rankings[-1] and self.rankings[-1].ranking != ranking.ranking

        if ranking_changed:
            # Extra data point for pretty lines up/down
            extra_ranking = Ranking(ranking.time - self.lead_in_seconds, self.rankings[-1].ranking)
            popped = None
            if self.rankings and self.rankings[-1].ranking != -1 and self.rankings[-1].time > extra_ranking.time and self.rankings[-1].ranking != ranking.ranking:
                popped = self.rankings.pop(-1)

                if not self.rankings:
                    # Popped the last point
                    # First approximation: put it back
                    # TODO: Move the line back according to imagined projection back?
                    extra_ranking = popped
                else:
                    # There is a previous point, intersect lines
                    previous = self.rankings[-1]
                    line1 = LineString([(previous.time, previous.ranking), (popped.time, popped.ranking)])
                    line2 = LineString([(extra_ranking.time + (extra_ranking.time - ranking.time), extra_ranking.ranking + (extra_ranking.ranking - ranking.ranking)), (ranking.time, ranking.ranking)])
                    geom = line1.intersection(line2)
                    # TODO improve test!
                    extra_ranking = Ranking(geom.x, geom.y) if geom.geom_type is 'Point' else None

            if extra_ranking:
                self.rankings.append(extra_ranking)

        if ranking_changed or not self.rankings:
            self.rankings.append(ranking)

    def retire(self, time):
        # TODO Should intersect this really
        retirement_rank = self.rankings[-1].ranking
        while self.rankings and self.rankings[-1].ranking != -1 and self.rankings[-1].time > time:
            self.rankings.pop(-1)

        self.rankings.append(Ranking(time, retirement_rank))
        self.rankings.append(Ranking(time, -1))

    def write_final_rank(self, time):
        if self.is_active(time) and self.rankings[-1]:
            self.rankings.append(Ranking(time, self.rankings[-1].ranking))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.name


class Analysis:

    def __init__(self, importance = 25, retire_days = 60, lead_in_seconds = 16 * 60 * 60, teams = {}):
        self.importance = importance
        self.retire_seconds = retire_days * day_seconds
        self.lead_in_seconds = lead_in_seconds
        self.player_to_team = dict((v, k) for k in teams for v in teams[k])
        self.players = {}

    def get_player(self, name):
        if self.player_to_team:
            name = self.player_to_team[name] if name in self.player_to_team else name
        if name in self.players:
            return self.players[name]
        else:
            player = self.players[name] = Player(name, self.retire_seconds, self.lead_in_seconds)
            return player

    def game_played(self, game):
        players_by_retirement = defaultdict(set)
        for retired_player in [p for p in self.players.values() if not p.is_active(game.time) and not p.is_retired()]:
            players_by_retirement[retired_player.most_recent_game].add(retired_player)

        for most_recent_game in sorted(players_by_retirement.keys()):
            time = most_recent_game + self.retire_seconds
            retired_players = players_by_retirement[most_recent_game]
            for retired_player in retired_players:
                retired_player.retire(time - self.lead_in_seconds)
            retired_player_names = set([p.name for p in retired_players])
            self.update_rankings(time, sorted([p for p in self.players.values() if p.is_active(time) and p.name not in retired_player_names], key=lambda x: x.elo, reverse=True))

        blue = self.get_player(game.blue_player)
        red = self.get_player(game.red_player)

        predict = 1 / (1 + 10 ** ((red.elo - blue.elo) / 180))
        result = game.blue_score / (game.blue_score + game.red_score)
        delta = self.importance * (result - predict)

        blue.game(delta, game.time)
        red.game(-delta, game.time)

        self.update_rankings(game.time, sorted([p for p in self.players.values() if p.is_active(game.time)], key=lambda x: x.elo, reverse=True))

    def update_rankings(self, time, ranked_players):
        rank = 1
        for player in ranked_players:
            player.update_ranking(Ranking(time, rank))
            rank +=1

    def process_games(self, time=None, flush=False):
        if flush:
            for player in self.players.values():
                player.write_final_rank((datetime.datetime.now() - __epoch__).total_seconds())


class RankingsEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Player):
            return {'label': obj.name, 'elo': '{0:.3f}'.format(obj.elo), 'data': obj.rankings, 'last': obj.most_recent_game * 1000}
        if isinstance(obj, Ranking):
            return [obj.time * 1000, obj.ranking] if obj.ranking != -1 else None
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
