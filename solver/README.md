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

## not done yet

- picking the best move (max node)
- depth limit
- heuristic

## tests

run from the repo root.

```
python -m unittest
```
