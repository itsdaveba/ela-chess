import pytest

from chess import Piece


def test_piece():
    assert len(Piece) == 6

    assert Piece.PAWN.to_char() == "P"
    assert Piece.KNIGHT.to_char() == "N"
    assert Piece.BISHOP.to_char() == "B"
    assert Piece.ROOK.to_char() == "R"
    assert Piece.QUEEN.to_char() == "Q"
    assert Piece.KING.to_char() == "K"

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
