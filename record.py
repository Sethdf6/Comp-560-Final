# plays one solver game and saves every step so it can be replayed
#
# python3 record.py --depth 3 --seed 29 --out demo/game.json

import argparse
import json
import os
import random
import time

from game.game_state import GameState
from solver.expectimax import best_move
from solver.heuristic import evaluate


def record_game(depth, seed):
    random.seed(seed)
    game = GameState()
    start = time.time()

    record = {
        "depth": depth,
        "seed": seed,
        "start": [row.copy() for row in game.board.grid],
        "steps": [],
    }

    while not game.game_over:
        direction = best_move(game.board, evaluate, depth)
        if direction is None:
            break

        game.move(direction)
        record["steps"].append({
            "move": direction,
            "board": [row.copy() for row in game.board.grid],
            "score": game.score,
        })

        if len(record["steps"]) % 200 == 0:
            print(len(record["steps"]), "moves, score", game.score, flush=True)

    record["score"] = game.score
    record["max_tile"] = game.board.get_max_tile()
    record["seconds"] = round(time.time() - start, 1)
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--depth", type=int, default=3)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--out", default=os.path.join("demo", "game.json"))
    args = parser.parse_args()

    record = record_game(args.depth, args.seed)

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    with open(args.out, "w") as file:
        json.dump(record, file)

    print("moves:", len(record["steps"]))
    print("score:", record["score"])
    print("max tile:", record["max_tile"])
    print("saved to", args.out)


if __name__ == "__main__":
    main()
