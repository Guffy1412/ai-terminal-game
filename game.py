SIZE = 5
START = (0, 0)


def draw(player):
    for y in range(SIZE):
        print(" ".join("P" if (x, y) == player else "." for x in range(SIZE)))
    print()


def main():
    player = START
    while True:
        draw(player)
        command = input("> ").strip().lower()
        if command in ("q", "quit"):
            break


if __name__ == "__main__":
    main()
