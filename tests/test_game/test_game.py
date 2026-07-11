import pytest

from chess import ChessGame, Move


def test_game():
    game = ChessGame()
    assert repr(game) == "ChessGame(history=[])"

    fen = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
    game = ChessGame(fen)
    assert repr(game) == f"ChessGame(fen='{fen}', history=[])"

    assert not game.make_move(Move.from_string("e2e4"))
    assert not game.make_move(Move.from_string("e4e5"))
    assert game.make_move(Move.from_string("d2d4"))
    assert repr(game) == f"ChessGame(fen='{fen}', history=[Move.D2D4])"

    game.undo_move()
    assert repr(game) == f"ChessGame(fen='{fen}', history=[])"

    with pytest.raises(ValueError, match="no previous move"):
        game.undo_move()
