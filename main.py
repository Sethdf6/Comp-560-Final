
from game.game_state import GameState

game = GameState()
print(game.board)

while not game.game_over:
    direction = input("move (left, right, up, down): ").lower()

    if direction not in ["left", "right", "up", "down"]:
        print("Invalid direction. Try again.")
        continue

    moved = game.move(direction)

    if not moved:
        print("No movement possible in that direction.")
        continue

    print(game.board)
    print("Score:", game.score)
    print("Maximum Tile:", game.board.get_max_tile())

print("Game Over")
print("Final Score:", game.score)
print("Highest Tile:", game.board.get_max_tile())
