from io import StringIO

from chess import ChessGame


def test_game(monkeypatch):
    game = ChessGame()

    monkeypatch.setattr("sys.stdin", StringIO("resign\n"))
    assert game.play(None, "human", "engine") == "White resigns: 0-1"

    monkeypatch.setattr("sys.stdin", StringIO("f5h5\n"))
    assert game.play("7k/8/8/5Q2/8/8/8/4K1R1 w - - 0 1", "human", "engine") == "White wins: 1-0"

    monkeypatch.setattr("sys.stdin", StringIO("f5g6\n"))
    assert game.play("7k/8/8/5Q2/8/8/8/4K1R1 w - - 0 1", "human", "engine") == "Draw: 1/2-1/2"

    monkeypatch.setattr("sys.stdin", StringIO("f5f8\nf8g7\n"))
    assert game.play("7k/8/8/5Q2/8/8/8/4K1R1 w - - 0 1", "human", "engine") == "White wins: 1-0"

    monkeypatch.setattr("sys.stdin", StringIO("f5f8\nf8g7\n"))
    assert game.play("7k/8/8/5Q2/8/8/8/4K1R1 w - - 97 1", "human", "engine") == "White wins: 1-0"

    monkeypatch.setattr("sys.stdin", StringIO("f5f8\n"))
    assert game.play("7k/8/8/5Q2/8/8/8/4K1R1 w - - 98 1", "human", "engine") == "Draw: 1/2-1/2"
