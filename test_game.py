import game


def test_grid_is_5x5(capsys):
    game.draw(game.START)
    rows = capsys.readouterr().out.strip().splitlines()
    assert game.SIZE == 5
    assert len(rows) == 5
    assert all(len(row.split()) == 5 for row in rows)


def test_player_starts_at_origin():
    assert game.START == (0, 0)


def test_player_drawn_at_top_left(capsys):
    game.draw(game.START)
    rows = capsys.readouterr().out.strip().splitlines()
    assert rows[0].split()[0] == game.PLAYER
    assert sum(row.count(game.PLAYER) for row in rows) == 1


def test_move_wasd():
    assert game.move((2, 2), "w") == (2, 1)
    assert game.move((2, 2), "a") == (1, 2)
    assert game.move((2, 2), "s") == (2, 3)
    assert game.move((2, 2), "d") == (3, 2)


def test_move_blocked_at_edges():
    assert game.move((0, 0), "w") == (0, 0)
    assert game.move((0, 0), "a") == (0, 0)
    assert game.move((4, 4), "s") == (4, 4)
    assert game.move((4, 4), "d") == (4, 4)


def test_move_ignores_other_input():
    assert game.move((2, 2), "x") == (2, 2)


def test_spawn_item_in_grid_and_not_on_player():
    for _ in range(200):
        item = game.spawn_item((2, 2))
        assert item != (2, 2)
        assert 0 <= item[0] < game.SIZE and 0 <= item[1] < game.SIZE


def test_draw_shows_item(capsys):
    game.draw((0, 0), (3, 1))
    rows = capsys.readouterr().out.strip().splitlines()
    assert rows[1].split()[3] == game.COLLECTIBLE


def run_game(monkeypatch, capsys, items, inputs, hazard=(2, 4)):
    items = iter(items)
    inputs = iter([""] + list(inputs))  # "" answers the intro screen
    monkeypatch.setattr(game, "spawn_item", lambda *args: next(items))
    monkeypatch.setattr(game, "spawn_hazard", lambda *args: hazard)
    monkeypatch.setattr(game.os, "system", lambda cmd: 0)

    def fake_input(prompt=""):
        print(prompt, end="")  # real input() writes its prompt to stdout
        return next(inputs)

    monkeypatch.setattr("builtins.input", fake_input)
    game.main()
    return capsys.readouterr().out


def test_score_increases_on_collect(monkeypatch, capsys):
    out = run_game(monkeypatch, capsys, [(1, 0), (4, 4)], ["d", "q"])
    assert "Score: 0" in out
    assert "Score: 1" in out


def test_item_respawns_after_collect(monkeypatch, capsys):
    out = run_game(monkeypatch, capsys, [(1, 0), (4, 4)], ["d", "q"])
    last_grid = out.strip().split("Score: 1")[0].strip().splitlines()[-5:]
    assert last_grid[4].split()[4] == game.COLLECTIBLE


def test_win_at_ten(monkeypatch, capsys):
    # item alternates between (1,0) and (0,0); player bounces d, a, d, a...
    items = [(1, 0), (0, 0)] * 5
    out = run_game(monkeypatch, capsys, items, ["d", "a"] * 5 + ["n"])
    assert game.WIN_MESSAGE in out and "Final score: 10" in out


def test_no_win_before_ten(monkeypatch, capsys):
    items = [(1, 0), (0, 0)] * 4 + [(4, 4)]
    out = run_game(monkeypatch, capsys, items, ["d", "a"] * 4 + ["q"])
    assert "You win" not in out
    assert "Score: 8" in out


def test_hazard_spawns_on_empty_cell():
    for _ in range(200):
        hazard = game.spawn_hazard((0, 0), (1, 1))
        assert hazard not in ((0, 0), (1, 1))
        assert 0 <= hazard[0] < game.SIZE and 0 <= hazard[1] < game.SIZE


def test_item_never_spawns_on_hazard():
    for _ in range(200):
        assert game.spawn_item((0, 0), (1, 1)) not in ((0, 0), (1, 1))


def test_draw_shows_hazard(capsys):
    game.draw((0, 0), (3, 1), (2, 2))
    rows = capsys.readouterr().out.strip().splitlines()
    assert rows[2].split()[2] == game.HAZARD


def test_hazard_ends_game(monkeypatch, capsys):
    # hazard at (1,0): the first move ends the game; "n" declines a replay
    out = run_game(monkeypatch, capsys, [(4, 4)], ["d", "n", "d"], hazard=(1, 0))
    assert game.LOSE_MESSAGE in out
    assert out.count("Score:") == 1


def test_hazard_not_triggered_elsewhere(monkeypatch, capsys):
    out = run_game(monkeypatch, capsys, [(4, 4)], ["s", "d", "q"], hazard=(0, 4))
    assert game.LOSE_MESSAGE not in out
    assert out.count("Score:") == 3


def test_hazard_stays_in_place(monkeypatch, capsys):
    out = run_game(monkeypatch, capsys, [(4, 4)], ["d", "s", "q"], hazard=(3, 3))
    assert out.count(game.HAZARD) == 3


def test_hazard_game_over_stops_loop(monkeypatch, capsys):
    inputs = iter(["", "d", "n", "extra"])
    monkeypatch.setattr(game, "spawn_item", lambda *args: (4, 4))
    monkeypatch.setattr(game, "spawn_hazard", lambda *args: (1, 0))
    monkeypatch.setattr(game.os, "system", lambda cmd: 0)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    game.main()  # returns instead of looping
    assert next(inputs) == "extra"  # nothing was read after answering n


def test_play_again_prompt_after_win(monkeypatch, capsys):
    items = [(1, 0), (0, 0)] * 5
    out = run_game(monkeypatch, capsys, items, ["d", "a"] * 5 + ["n"])
    assert "Play again? (y/n)" in out


def test_play_again_prompt_after_lose(monkeypatch, capsys):
    out = run_game(monkeypatch, capsys, [(4, 4)], ["d", "n"], hazard=(1, 0))
    assert "Play again? (y/n)" in out


def test_no_prompt_when_quitting(monkeypatch, capsys):
    out = run_game(monkeypatch, capsys, [(4, 4)], ["q"])
    assert "Play again?" not in out


def test_play_again_y_resets_game(monkeypatch, capsys):
    # lose at (1,0) with a score of 1, say y, then quit the fresh game
    items = [(0, 1), (4, 4), (4, 4)]
    inputs = ["s", "w", "d", "y", "q"]
    out = run_game(monkeypatch, capsys, items, inputs, hazard=(1, 0))
    frames = out.split("Score: ")
    assert frames[1].startswith("0") and frames[2].startswith("1")
    assert frames[-1].startswith("0")  # score reset in the new game
    assert out.count(game.LOSE_MESSAGE) == 1
    # new game starts with the player back at (0,0)
    last_grid = out.rsplit("Score: ", 1)[0].strip().splitlines()[-5:]
    assert last_grid[0].endswith(f"{game.PLAYER} {game.HAZARD} " + " ".join([game.EMPTY] * 3))  # follows the unterminated prompt line


def test_play_again_reprompts_on_invalid(monkeypatch, capsys):
    out = run_game(monkeypatch, capsys, [(4, 4)], ["d", "maybe", "n"], hazard=(1, 0))
    assert out.count("Play again?") == 2  # asked again after the invalid answer


def patch_play(monkeypatch, items, inputs, hazard=(2, 4)):
    items, inputs = iter(items), iter(inputs)
    monkeypatch.setattr(game, "spawn_item", lambda *args: next(items))
    monkeypatch.setattr(game, "spawn_hazard", lambda *args: hazard)
    monkeypatch.setattr(game.os, "system", lambda cmd: 0)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))


def test_play_returns_win(monkeypatch):
    patch_play(monkeypatch, [(1, 0), (0, 0)] * 5, ["d", "a"] * 5)
    assert game.play() == "win"


def test_play_returns_lose(monkeypatch):
    patch_play(monkeypatch, [(4, 4)], ["d"], hazard=(1, 0))
    assert game.play() == "lose"


def test_play_returns_quit(monkeypatch):
    patch_play(monkeypatch, [(4, 4)], ["q"])
    assert game.play() == "quit"


def test_play_again_answers(monkeypatch):
    answers = iter(["maybe", "", "Y"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))
    assert game.play_again() is True
    answers = iter(["N"])
    assert game.play_again() is False


def test_multiple_replays(monkeypatch, capsys):
    # lose, replay, lose, replay, lose, decline
    out = run_game(monkeypatch, capsys, [(4, 4)] * 3,
                   ["d", "y", "d", "y", "d", "n"], hazard=(1, 0))
    assert out.count(game.LOSE_MESSAGE) == 3


def test_intro_shows_title_and_story(monkeypatch, capsys):
    out = run_game(monkeypatch, capsys, [(4, 4)], ["q"])
    assert game.TITLE in out
    assert game.STORY in out
    assert "Press Enter to begin" in out


def test_intro_shown_once_across_replays(monkeypatch, capsys):
    out = run_game(monkeypatch, capsys, [(4, 4)] * 2, ["d", "y", "d", "n"], hazard=(1, 0))
    assert out.count(game.TITLE) == 1


def test_emoji_symbols_are_distinct():
    symbols = {game.PLAYER, game.COLLECTIBLE, game.HAZARD, game.EMPTY}
    assert len(symbols) == 4


def test_theme_text_is_set():
    for text in (game.TITLE, game.STORY, game.WIN_MESSAGE, game.LOSE_MESSAGE):
        assert isinstance(text, str) and text.strip()


def test_full_grid_uses_theme_symbols(capsys):
    game.draw((0, 0), (4, 4), (2, 2))
    rows = [row.split() for row in capsys.readouterr().out.strip().splitlines()]
    cells = [cell for row in rows for cell in row]
    assert cells.count(game.PLAYER) == 1
    assert cells.count(game.COLLECTIBLE) == 1
    assert cells.count(game.HAZARD) == 1
    assert cells.count(game.EMPTY) == 22
    assert rows[0][0] == game.PLAYER and rows[4][4] == game.COLLECTIBLE and rows[2][2] == game.HAZARD


def test_win_message_includes_score(monkeypatch, capsys):
    out = run_game(monkeypatch, capsys, [(1, 0), (0, 0)] * 5, ["d", "a"] * 5 + ["n"])
    assert f"{game.WIN_MESSAGE} Final score: 10" in out


def test_score_line_uses_theme_grid_each_turn(monkeypatch, capsys):
    out = run_game(monkeypatch, capsys, [(4, 4)], ["d", "s", "q"])
    assert out.count("Score: 0") == 3
    assert out.count(game.PLAYER) == 3
