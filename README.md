# SameGame

Single player game with a twist. Beat the AI based on **Monte Carlo Tree Search** alogrithm.

## Game rules

* Adjacent tiles of the same color form a region.
* The goal is to remove as big as possible regions of tiles of the same color.
* There must be at least 2 tiles in region to be removed. The game is over when there are no more moves left.
* You get points after removing region. Points of $n$-tile region are counted as follows: $\text{points} = (n-2)^2$.

## Beat AI

Your main goal is to beat the AI. Let's call it Mike. You and Mike get the same board on start. Mike's move is revealed after your move. Whoever has more points at the end wins.

## AI settings

Mike doesn't always has a good day. He sometimes makes mistakes.
He has his own value of infallibility.
The greater value you set, the less mistakes he will make.
Also, the greater value you set, the more time it takes for Mike to choose and make a move.