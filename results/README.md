# results

200 games per agent, seeds 0 to 199, 4x4 board.
every row of `games.csv` is one game.

rerun from the repo root.

```
python3 experiments.py --games 200
python3 experiments.py --summary
python3 results/plot.py
```

`plot.py` draws `chart.png` and needs matplotlib.

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
| random | 200 | 1154 | 1152 | 0% | 0% | 0% | 0% | 122 |
| greedy | 200 | 3216 | 2778 | 17% | 2% | 0% | 0% | 260 |
| expectimax d1 | 200 | 3200 | 2768 | 14% | 2% | 0% | 0% | 261 |
| expectimax d2 | 200 | 15674 | 14788 | 97% | 75% | 26% | 0% | 888 |
| expectimax d3 | 200 | 23124 | 24660 | 99% | 94% | 59% | 2% | 1235 |
| d2 snake only | 200 | 21188 | 16870 | 95% | 78% | 46% | 6% | 1130 |
| d2 empty only | 200 | 9978 | 7710 | 94% | 47% | 1% | 0% | 624 |
| d3 snake only | 200 | 27575 | 27312 | 99% | 94% | 64% | 10% | 1431 |

## time per move

one core on an idle machine, boards sampled from depth 2 games.

| depth | ms per move |
|---|---|
| 1 | 0.07 |
| 2 | 5 |
| 3 | 190 |

the `seconds` column in the csv was measured with 14 games running at once, so it is slower than this.

## what we see

- search depth matters most. 2048 is reached in 0% of games at depth 1, 26% at depth 2 and 59% at depth 3.
- depth 1 is almost the same as greedy. they got the same score in 108 of 200 seeds. one level of chance does not change the choice much.
- each extra level costs about 30 to 80 times more time.
- the snake part of the heuristic does the work. empty cells alone reached 2048 in 1 of 200 games.
- the empty cell bonus hurts. at depth 2 snake only reaches 2048 in 46% of games, snake with the bonus in 26%.
- at depth 3 the gap is smaller. 2048 is reached in 64% against 59%, which is close. the average score is 27575 against 23124, and 4096 is reached in 19 games against 3.
- the best agent is depth 3 with snake only. it reached 4096 in 19 of 200 games. no agent reached 8192.

the first run had 50 games per agent. the depth 3 gap for 2048 looked bigger there, 72% against 52%.
the other findings stayed the same with 200 games.
