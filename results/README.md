# results

50 games per agent, seeds 0 to 49, 4x4 board.
every row of `games.csv` is one game.

rerun from the repo root.

```
python3 experiments.py
python3 experiments.py --summary
```

## agents

- random: any legal move
- greedy: best move by heuristic, no search
- expectimax d1, d2, d3: search depth in player moves
- d2 snake only, d2 empty only, d3 snake only: one part of the heuristic

greedy and expectimax d1 to d3 use `snake_with_bonus`, the first heuristic we tried.
it is the snake score times a bonus for every empty cell.
the solver now uses the snake score alone, because it did better here.

## table

the tile columns show the share of games that reached that tile.

| agent | games | avg score | median score | 512 | 1024 | 2048 | 4096 | avg moves |
|---|---|---|---|---|---|---|---|---|
| random | 50 | 1112 | 1188 | 0% | 0% | 0% | 0% | 120 |
| greedy | 50 | 2971 | 2588 | 12% | 0% | 0% | 0% | 246 |
| expectimax d1 | 50 | 3026 | 2576 | 14% | 0% | 0% | 0% | 248 |
| expectimax d2 | 50 | 15605 | 14644 | 98% | 76% | 24% | 0% | 888 |
| expectimax d3 | 50 | 22976 | 24136 | 98% | 92% | 52% | 2% | 1231 |
| d2 snake only | 50 | 19452 | 18324 | 94% | 72% | 48% | 2% | 1047 |
| d2 empty only | 50 | 10051 | 7676 | 90% | 48% | 2% | 0% | 627 |
| d3 snake only | 50 | 29332 | 32508 | 98% | 94% | 72% | 10% | 1513 |

## time per move

one core, boards sampled from one depth 2 game.

| depth | ms per move |
|---|---|
| 1 | 0.1 |
| 2 | 9 |
| 3 | 285 |

the `seconds` column in the csv was measured with 14 games running at once, so it is slower than this.

## what we see

- search depth matters most. 2048 is reached in 0% of games at depth 1, 24% at depth 2 and 52% at depth 3.
- depth 1 is almost the same as greedy. they got the same score in 32 of 50 seeds. one level of chance does not change the choice much.
- each extra level costs about 30 to 80 times more time.
- the snake part of the heuristic does the work. empty cells alone reach 2048 in 2% of games.
- the empty cell bonus hurts. snake only reaches 2048 in 48% of games at depth 2 and 72% at depth 3, snake with the bonus in 24% and 52%.
- the best agent is depth 3 with snake only. it reached 4096 in 5 of 50 games.

50 games is a small sample, so close numbers can swap.
