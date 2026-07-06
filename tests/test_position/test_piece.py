import pytest

from chess import Piece


def test_piece():
    assert len(Piece) == 8

    assert Piece.PAWN.char == "P"
    assert Piece.KNIGHT.char == "N"
    assert Piece.BISHOP.char == "B"
    assert Piece.ROOK.char == "R"
    assert Piece.QUEEN.char == "Q"
    assert Piece.KING.char == "K"
    assert Piece.NONE.char == "."
    assert Piece.OFF.char == "*"

    with pytest.raises(ValueError, match="invalid piece char"):
        assert Piece.from_char(".")

    assert Piece.from_char("P") == Piece.PAWN
    assert Piece.from_char("N") == Piece.KNIGHT
    assert Piece.from_char("B") == Piece.BISHOP
    assert Piece.from_char("R") == Piece.ROOK
    assert Piece.from_char("Q") == Piece.QUEEN
    assert Piece.from_char("K") == Piece.KING
