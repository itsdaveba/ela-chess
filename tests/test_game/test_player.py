import io

from chess import HumanPlayer, EnginePlayer, ChessGame, Move


def test_player(monkeypatch):
    game = ChessGame()

    # human
    player = HumanPlayer()
    assert repr(player) == "Human"

    monkeypatch.setattr('sys.stdin', io.StringIO("e2e4"))
    move = player.search(game, -1, -1, -1)
    assert move == "e2e4"

    # engine
    player = EnginePlayer()
    assert repr(player) == "Engine"

    move = player.search(game, -1, 1, -1)
    assert isinstance(move, Move)
