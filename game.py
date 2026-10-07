import os
import random

SIZE = 5
START = (0, 0)
WIN_SCORE = 10
MOVES = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0)}


def draw(player, item=None, hazard=None):
    symbols = {player: "P", hazard: "X", item: "*"}
    for y in range(SIZE):
        print(" ".join(symbols.get((x, y), ".") for x in range(SIZE)))
    print()


def move(player, command):
    dx, dy = MOVES.get(command, (0, 0))
    x, y = player[0] + dx, player[1] + dy
    if 0 <= x < SIZE and 0 <= y < SIZE:
        return (x, y)
    return player


def spawn_item(player, hazard=None):
    cells = [(x, y) for x in range(SIZE) for y in range(SIZE)
             if (x, y) not in (player, hazard)]
    return random.choice(cells)


def spawn_hazard(player, item):
    cells = [(x, y) for x in range(SIZE) for y in range(SIZE)
             if (x, y) not in (player, item)]
    return random.choice(cells)


def main():
    player = START
    item = spawn_item(player)
    hazard = spawn_hazard(player, item)
    score = 0
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        draw(player, item, hazard)
        print(f"Score: {score}")
        command = input("> ").strip().lower()
        if command in ("q", "quit"):
            break
        player = move(player, command)
        if player == hazard:
            print("Game Over!")
            break
        if player == item:
            score += 1
            if score >= WIN_SCORE:
                print(f"You win! Final score: {score}")
                break
            item = spawn_item(player, hazard)


if __name__ == "__main__":
    main()
