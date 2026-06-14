import pytest

from chess import Castling


def test_castling():
    with pytest.raises(ValueError, match="invalid castling value"):
        Castling(-1)
    with pytest.raises(ValueError, match="invalid castling string"):
        Castling("")
    with pytest.raises(ValueError, match="invalid castling string"):
        Castling("QK")

    castling = Castling(15)
    assert repr(castling) == "Castling('KQkq')"
    assert castling.rights == 15
    assert castling.string == "KQkq"
    assert castling & "K"

    castling = Castling("-")
    assert repr(castling) == "Castling('-')"
    assert castling.rights == 0
    assert castling.string == "-"
    assert not castling & "kq"

    castling = Castling("Kq")
    assert repr(castling) == "Castling('Kq')"
    assert castling.rights == 9
    assert castling.string == "Kq"
    assert castling & "KQ"
