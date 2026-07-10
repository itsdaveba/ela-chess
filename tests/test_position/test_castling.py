import pytest

from chess import Castling


def test_castling():
    assert len(Castling) == 5

    assert Castling.WHITE_KINGSIDE.string == "K"
    assert Castling.WHITE_QUEENSIDE.string == "Q"
    assert Castling.BLACK_KINGSIDE.string == "k"
    assert Castling.BLACK_QUEENSIDE.string == "q"
    assert Castling.NONE.string == "-"
    assert not Castling.NONE

    assert (Castling.BLACK_QUEENSIDE | Castling.WHITE_KINGSIDE).string == "Kq"

    with pytest.raises(ValueError, match="invalid castling string"):
        assert Castling.from_string("qK")

    assert Castling.from_string("K") == Castling.WHITE_KINGSIDE
    assert Castling.from_string("Q") == Castling.WHITE_QUEENSIDE
    assert Castling.from_string("k") == Castling.BLACK_KINGSIDE
    assert Castling.from_string("q") == Castling.BLACK_QUEENSIDE
    assert Castling.from_string("-") == Castling.NONE

    assert Castling.from_string("Kq") == Castling.BLACK_QUEENSIDE | Castling.WHITE_KINGSIDE
