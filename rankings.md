Rankings strategy
=================

Aim is to show the (table football) ranks of active players over time, like the "race to the finish" style F1 charts after each race.
It's much harder with this data as there aren't consistent spaces between games.

Requirements
------------

* Show only active players
* Discontinuous graph when player retires (so that they can't play a single game in the future and get re-ranked in the past)
* Look pretty
** Use a "lead-in time" so that changes in rank don't have a vertical gradient
** When players start, retire or comeback, point should not intersect with another line
* Preserve as much data as possible (e.g. partial changes in rank that are reversed)

Strategies
----------

* When a player retires, their line is terminated ${lead_in_seconds} before their actual retirement time. This is to leave a gap for the
  player that occupies their old rank to move into.
* When a player starts, retires or comes back, the time position of their line may not be moved. This would cause near vertical changes
  in rank e.g. if they appear, and then lose the next game an hour later and lose places. The strategy here is to draw the graph as if it
  has a normal lead-in, but then crop the lead-in at the exact time they appeared. Similarly for retirements (but these are most times
  smaller changes in rank and don't look as bad). (NOTE: at the time of writing we don't actually process retirements in this way: TODO).
