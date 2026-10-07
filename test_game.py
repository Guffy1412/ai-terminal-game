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
