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
    assert rows[0].split()[0] == "P"
    assert sum(row.count("P") for row in rows) == 1


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
    assert rows[1].split()[3] == "*"


def run_game(monkeypatch, capsys, items, inputs, hazard=(2, 4)):
    items = iter(items)
    inputs = iter(inputs)
    monkeypatch.setattr(game, "spawn_item", lambda *args: next(items))
    monkeypatch.setattr(game, "spawn_hazard", lambda *args: hazard)
    monkeypatch.setattr(game.os, "system", lambda cmd: 0)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    game.main()
    return capsys.readouterr().out


def test_score_increases_on_collect(monkeypatch, capsys):
    out = run_game(monkeypatch, capsys, [(1, 0), (4, 4)], ["d", "q"])
    assert "Score: 0" in out
    assert "Score: 1" in out


def test_item_respawns_after_collect(monkeypatch, capsys):
    out = run_game(monkeypatch, capsys, [(1, 0), (4, 4)], ["d", "q"])
    last_grid = out.strip().split("Score: 1")[0].strip().splitlines()[-5:]
    assert last_grid[4].split()[4] == "*"


def test_win_at_ten(monkeypatch, capsys):
    # item alternates between (1,0) and (0,0); player bounces d, a, d, a...
    items = [(1, 0), (0, 0)] * 5
    out = run_game(monkeypatch, capsys, items, ["d", "a"] * 5)
    assert "You win! Final score: 10" in out


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
    assert rows[2].split()[2] == "X"


def test_hazard_ends_game(monkeypatch, capsys):
    # hazard at (1,0): the first move ends the game, so the 2nd input is never read
    out = run_game(monkeypatch, capsys, [(4, 4)], ["d", "d"], hazard=(1, 0))
    assert "Game Over!" in out
    assert out.count("Score:") == 1


def test_hazard_not_triggered_elsewhere(monkeypatch, capsys):
    out = run_game(monkeypatch, capsys, [(4, 4)], ["s", "d", "q"], hazard=(0, 4))
    assert "Game Over!" not in out
    assert out.count("Score:") == 3


def test_hazard_stays_in_place(monkeypatch, capsys):
    out = run_game(monkeypatch, capsys, [(4, 4)], ["d", "s", "q"], hazard=(3, 3))
    assert out.count("X") == 3


def test_hazard_game_over_stops_loop(monkeypatch, capsys):
    inputs = iter(["d", "q"])
    monkeypatch.setattr(game, "spawn_item", lambda *args: (4, 4))
    monkeypatch.setattr(game, "spawn_hazard", lambda *args: (1, 0))
    monkeypatch.setattr(game.os, "system", lambda cmd: 0)
    monkeypatch.setattr("builtins.input", lambda prompt="": next(inputs))
    game.main()  # returns instead of looping
    assert next(inputs) == "q"  # the second input was never consumed
