from io import StringIO

from chess import Position, Human, Engine


def test_human(monkeypatch):
    player = Human()
    position = Position()

    assert repr(player) == "Human(uci=False)"

    monkeypatch.setattr("sys.stdin", StringIO("\nundo\ne2e2\ne2e4"))
    move = player.search(position)
    assert move == "e2e4"

    position.make_move(move)
    monkeypatch.setattr("sys.stdin", StringIO("e7e5"))
    move = player.search(position)
    assert move == "e7e5"

    position.make_move(move)
    monkeypatch.setattr("sys.stdin", StringIO("undo\nresign\n"))
    move = player.search(position)
    assert move is None


def test_engine():
    position = Position()

    player = Engine(uci=True)
    assert repr(player) == "Engine(uci=True)"
    move = player.search(position)
    assert move is not None

    player = Engine(uci=False)
    assert repr(player) == "Engine(uci=False)"
    move = player.search(position)
    assert move is not None
