import pytest

from chess import Piece


def test_piece():
    assert len(Piece) == 8

    assert not Piece.PAWN.is_sliding
    assert Piece.PAWN.char == "P"

    assert not Piece.KNIGHT.is_sliding
    assert Piece.KNIGHT.char == "N"

    assert Piece.BISHOP.is_sliding
    assert Piece.BISHOP.char == "B"

    assert Piece.ROOK.is_sliding
    assert Piece.ROOK.char == "R"

    assert Piece.QUEEN.is_sliding
    assert Piece.QUEEN.char == "Q"

    assert not Piece.KING.is_sliding
    assert Piece.KING.char == "K"

    assert not Piece.OFF.is_sliding
    assert Piece.OFF.char == "#"

    assert not Piece.NONE.is_sliding
    assert Piece.NONE.char == "."

    with pytest.raises(ValueError, match="invalid piece char"):
        assert Piece.from_char(".")

    assert Piece.from_char("P") == Piece.PAWN
    assert Piece.from_char("N") == Piece.KNIGHT
    assert Piece.from_char("B") == Piece.BISHOP
    assert Piece.from_char("R") == Piece.ROOK
    assert Piece.from_char("Q") == Piece.QUEEN
    assert Piece.from_char("K") == Piece.KING
