# lets the solver play 2048 by itself
#
# python3 autoplay.py                 watch one game
# python3 autoplay.py --games 20      play 20 games and print a summary
# python3 autoplay.py --depth 3       search deeper, slower

import argparse
import random
import time

from game.game_state import GameState
from solver.expectimax import best_move
from solver.heuristic import evaluate


def play_game(depth, show=False):
    game = GameState()
    moves = 0
    start = time.time()

    if show:
        print(game.board)

    while not game.game_over:
        direction = best_move(game.board, evaluate, depth)
        if direction is None:
            break

        game.move(direction)
        moves += 1

        if show:
            print(direction)
            print(game.board)
            print("Score:", game.score)

    return {
        "score": game.score,
        "max_tile": game.board.get_max_tile(),
        "moves": moves,
        "seconds": time.time() - start,
    }


def print_summary(results):
    games = len(results)
    scores = [result["score"] for result in results]
    moves = sum(result["moves"] for result in results)
    seconds = sum(result["seconds"] for result in results)

    print("games:", games)
    print("average score:", round(sum(scores) / games))
    print("best score:", max(scores))
    print("ms per move:", round(1000 * seconds / max(moves, 1), 1))

    # share of games that reached each tile
    for tile in (512, 1024, 2048, 4096):
        reached = sum(result["max_tile"] >= tile for result in results)
        print(f"reached {tile}: {reached}/{games}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=1)
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    if args.games == 1:
        result = play_game(args.depth, show=True)
        print("Game Over")
        print("Final Score:", result["score"])
        print("Highest Tile:", result["max_tile"])
        print("Moves:", result["moves"])
        return

    results = []
    for number in range(1, args.games + 1):
        result = play_game(args.depth)
        results.append(result)
        print(f"game {number}: score {result['score']}, max tile {result['max_tile']}")

    print_summary(results)


if __name__ == "__main__":
    main()
