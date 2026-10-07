# Ember Hollow 🐉

A tiny terminal game written in pure Python. A storm has scattered your dragon's eggs across a volcano's crater. Guide the dragon around a 5x5 grid, rescue all 10 eggs, and stay clear of the lava.

```
🐉 ⬛ ⬛ ⬛ ⬛
⬛ ⬛ 🥚 ⬛ ⬛
⬛ ⬛ ⬛ ⬛ ⬛
⬛ ⬛ ⬛ 🌋 ⬛
⬛ ⬛ ⬛ ⬛ ⬛
Score: 0
>
```

| Symbol | Meaning |
|--------|---------|
| 🐉 | You, the dragon |
| 🥚 | An egg to rescue |
| 🌋 | The volcano. Touch it and the game is over |
| ⬛ | Empty ground |

## Features

- **WASD movement**: `W` up, `A` left, `S` down, `D` right (type the key, then press Enter). Moves that would leave the grid are ignored.
- **Collectible scoring**: One egg is on the board at a time. Reaching it adds 1 to your score and the egg respawns somewhere else. It never appears on you or on the volcano.
- **Hazard**: A volcano is placed on a random empty cell at the start of each game. Stepping on it ends the game immediately.
- **Win condition**: Rescue 10 eggs and the clutch is safe.
- **Lose condition**: Step on the volcano and it's game over.
- **Restart**: After a win or a loss you are asked `Play again? (y/n)`. `y` resets the player, score, egg and volcano for a fresh game. `n` exits cleanly.
- **Fresh screen every turn**: The terminal is cleared and the grid redrawn on each move, with the current score shown below it.
- **Quit any time**: Type `q` (or `quit`) during play.

## How to Run

### Requirements

- Python 3 (developed and tested on 3.12)
- A terminal that can display emoji (for example Windows Terminal, macOS Terminal or most Linux terminals)

### Play

```bash
python game.py
```

### Run the tests

The test suite uses [pytest](https://docs.pytest.org/):

```bash
pip install pytest
pytest
```

## Project Structure

```
.
├── game.py        # the game: grid, movement, scoring, hazard, replay loop
├── test_game.py   # pytest suite
└── README.md
```

## What I Learned

- **Iterative development**: The game was built in small steps rather than all at once: first a grid and input loop, then WASD movement, then a collectible with scoring, then a hazard, then a replay loop, and finally the theme. Each step was small enough to run and check before moving on, so problems were easy to locate.
- **Engineering prompts to prevent regression**: Each new request was written to name exactly what to add and to say what not to add (for example, "don't include additional features beyond this"). Asking for the existing behavior to keep working, and for tests to be re-run after every change, meant new features didn't quietly break old ones.
- **Automated tests**: A pytest suite grew alongside the game. Tests cover the grid, movement and boundaries, spawning, scoring, the win and lose conditions, and the play-again flow. Small design choices, such as keeping movement and spawning in their own functions and putting emoji and messages in named constants, made the game easy to test. When the hazard and the replay loop changed how the game was wired together, the existing tests showed exactly which ones needed updating, and the full suite passing again confirmed nothing else had broken.
