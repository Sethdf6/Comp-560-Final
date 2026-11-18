# plays many games with each agent and saves one row per game
#
# python3 experiments.py                          all agents, 50 games each
# python3 experiments.py --games 5 --agents random greedy
# python3 experiments.py --summary                only print the table
#
# games that are already in the csv are skipped, so a run can be resumed

import argparse
import csv
import os
import random
import statistics
import time
from multiprocessing import Pool

from game.game_mechanics import move_down, move_left, move_right, move_up
from game.game_state import GameState
from solver.expectimax import best_move
from solver.heuristic import evaluate, snake_score, snake_with_bonus

RESULTS_FILE = os.path.join("results", "games.csv")
FIELDS = ["agent", "seed", "score", "max_tile", "moves", "seconds"]

MOVES = (
    ("left", move_left),
    ("right", move_right),
    ("up", move_up),
    ("down", move_down),
)


def legal_moves(board):
    # (direction, board after the move, points gained), before the spawn
    options = []
    for direction, move in MOVES:
        moved, gained = move(board)
        if moved.grid != board.grid:
            options.append((direction, moved, gained))
    return options


def random_agent(board):
    # baseline 1, any legal move
    options = legal_moves(board)
    return random.choice(options)[0] if options else None


def greedy_agent(board):
    # baseline 2, heuristic only, no search and no chance node
    options = legal_moves(board)
    if not options:
        return None
    return max(options, key=lambda option: option[2] + snake_with_bonus(option[1]))[0]


def empty_cells(board):
    return len(board.get_empty_cells())


def expectimax_agent(depth, value_fn=evaluate):
    return lambda board: best_move(board, value_fn, depth)


AGENTS = {
    "random": random_agent,
    # these four use the snake score with the empty cell bonus
    "greedy": greedy_agent,
    "expectimax d1": expectimax_agent(1, snake_with_bonus),
    "expectimax d2": expectimax_agent(2, snake_with_bonus),
    "expectimax d3": expectimax_agent(3, snake_with_bonus),
    # one part of the heuristic at a time
    "d2 snake only": expectimax_agent(2, snake_score),
    "d2 empty only": expectimax_agent(2, empty_cells),
    "d3 snake only": expectimax_agent(3, snake_score),
}


def play(job):
    name, seed = job
    agent = AGENTS[name]

    # same seed gives every agent the same first two tiles
    random.seed(seed)
    game = GameState()
    moves = 0
    start = time.time()

    while not game.game_over:
        direction = agent(game.board)
        if direction is None:
            break
        game.move(direction)
        moves += 1

    return {
        "agent": name,
        "seed": seed,
        "score": game.score,
        "max_tile": game.board.get_max_tile(),
        "moves": moves,
        "seconds": round(time.time() - start, 2),
    }


def load_results():
    if not os.path.exists(RESULTS_FILE):
        return []
    with open(RESULTS_FILE, newline="") as file:
        return list(csv.DictReader(file))


def run(names, games, workers):
    os.makedirs(os.path.dirname(RESULTS_FILE), exist_ok=True)
    done = {(row["agent"], int(row["seed"])) for row in load_results()}
    jobs = [
        (name, seed)
        for name in names
        for seed in range(games)
        if (name, seed) not in done
    ]
    print(len(jobs), "games to play")
    if not jobs:
        return

    is_new = not os.path.exists(RESULTS_FILE)
    with open(RESULTS_FILE, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if is_new:
            writer.writeheader()

        with Pool(workers) as pool:
            for count, row in enumerate(pool.imap_unordered(play, jobs), 1):
                writer.writerow(row)
                file.flush()
                print(f"{count}/{len(jobs)} {row['agent']} seed {row['seed']}: "
                      f"score {row['score']}, max tile {row['max_tile']}", flush=True)


def summary_table():
    rows = load_results()
    lines = [
        "| agent | games | avg score | median score | 512 | 1024 | 2048 | 4096 | avg moves |",
        "|---|---|---|---|---|---|---|---|---|",
    ]

    for name in AGENTS:
        games = [row for row in rows if row["agent"] == name]
        if not games:
            continue

        count = len(games)
        scores = [int(row["score"]) for row in games]
        tiles = [int(row["max_tile"]) for row in games]
        moves = sum(int(row["moves"]) for row in games)

        # int(x + 0.5) rounds a half up, round() would send 0.5 to 0
        reached = [
            f"{int(100 * sum(tile >= goal for tile in tiles) / count + 0.5)}%"
            for goal in (512, 1024, 2048, 4096)
        ]
        lines.append(
            f"| {name} | {count} | {round(sum(scores) / count)} | {round(statistics.median(scores))} | "
            + " | ".join(reached)
            + f" | {round(moves / count)} |"
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=50)
    parser.add_argument("--agents", nargs="+", default=list(AGENTS), choices=list(AGENTS))
    parser.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()

    if not args.summary:
        run(args.agents, args.games, args.workers)

    print(summary_table())


if __name__ == "__main__":
    main()
