import io

from chess import HumanPlayer, EnginePlayer, Position, Move


def test_player(monkeypatch):
    position = Position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

    # human
    player = HumanPlayer()
    assert repr(player) == "Human"

    monkeypatch.setattr('sys.stdin', io.StringIO("e2e4"))
    move = player.best_move(position, -1, -1, -1)
    assert move == "e2e4"

    # engine
    player = EnginePlayer()
    assert repr(player) == "Engine"

    move = player.best_move(position, -1, 0, -1)
    assert isinstance(move, Move)
