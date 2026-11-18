# solver

## chance node

after every move the game adds one tile to a random empty cell.
it is a 2 with 90% odds and a 4 with 10% odds.

expectimax does not predict the tile.
it lists every option and takes the weighted average.
with 6 empty cells that is 12 boards.

```python
from game.game_mechanics import move_left
from solver.chance import spawn_outcomes, chance_value

moved, gained = move_left(board)

# a move that changes nothing is illegal, no tile spawns
if moved.grid != board.grid:
    # all boards the spawn can produce
    for odds, new_board in spawn_outcomes(moved):
        ...

    # expected value of the move for any scoring function
    value = chance_value(moved, my_heuristic)
```

`value_fn` can be a heuristic or the next level of the search.

## search

`best_move(board, evaluate, depth)` in `expectimax.py` returns left, right, up, down or None.
depth counts player moves.

## heuristic

`evaluate(board)` in `heuristic.py` scores a leaf board.
big tiles should follow a snake path from the top left corner.
`snake_with_bonus` also rewards empty cells, but it did worse in the experiments.

## autoplay

run from the repo root.

```
python3 autoplay.py
python3 autoplay.py --games 20
python3 autoplay.py --depth 3
```

depth 2 takes about 9 ms per move, depth 3 about 285 ms.
numbers from 50 games per agent are in `results/README.md`.

## tests

run from the repo root.

```
python -m unittest
```
