import pytest

from chess import Piece


def test_piece():
    assert len(Piece) == 7

    assert Piece.PAWN.char == "P"
    assert Piece.KNIGHT.char == "N"
    assert Piece.BISHOP.char == "B"
    assert Piece.ROOK.char == "R"
    assert Piece.QUEEN.char == "Q"
    assert Piece.KING.char == "K"
    assert Piece.NONE.char == "."

    with pytest.raises(ValueError, match="invalid piece char"):
        assert Piece.from_char("")
    with pytest.raises(ValueError, match="invalid piece char"):
        assert Piece.from_char("n")

    assert Piece.from_char("P") == Piece.PAWN
    assert Piece.from_char("N") == Piece.KNIGHT
    assert Piece.from_char("B") == Piece.BISHOP
    assert Piece.from_char("R") == Piece.ROOK
    assert Piece.from_char("Q") == Piece.QUEEN
    assert Piece.from_char("K") == Piece.KING
    assert Piece.from_char(".") == Piece.NONE
