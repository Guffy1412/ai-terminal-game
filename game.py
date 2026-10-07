import os
import random
import sys

TITLE = "Ember Hollow"
STORY = ("A storm shook your dragon's nest and scattered the eggs across the "
         "volcano's crater. "
         "Gather all 10 before the lava claims you!")
PLAYER = "🐉"
COLLECTIBLE = "🥚"
HAZARD = "🌋"
EMPTY = "⬛"
WIN_MESSAGE = "The clutch is safe! Every egg is back in the nest."
LOSE_MESSAGE = "Game Over! The volcano erupted and swallowed you whole."

SIZE = 5
START = (0, 0)
WIN_SCORE = 10
MOVES = {"w": (0, -1), "a": (-1, 0), "s": (0, 1), "d": (1, 0)}


def draw(player, item=None, hazard=None):
    symbols = {player: PLAYER, hazard: HAZARD, item: COLLECTIBLE}
    for y in range(SIZE):
        print(" ".join(symbols.get((x, y), EMPTY) for x in range(SIZE)))
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


def play():
    """Play one game. Returns "win", "lose" or "quit"."""
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
            return "quit"
        player = move(player, command)
        if player == hazard:
            print(LOSE_MESSAGE)
            return "lose"
        if player == item:
            score += 1
            if score >= WIN_SCORE:
                print(f"{WIN_MESSAGE} Final score: {score}")
                return "win"
            item = spawn_item(player, hazard)


def play_again():
    while True:
        answer = input("Play again? (y/n) ").strip().lower()
        if answer in ("y", "n"):
            return answer == "y"


def intro():
    print(f"=== {TITLE} ===")
    print()
    print(STORY)
    print()
    input("Press Enter to begin...")


def main():
    intro()
    while play() != "quit" and play_again():
        pass


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # emoji on Windows consoles
    main()
