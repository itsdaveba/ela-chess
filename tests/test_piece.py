import pytest

from chess import PieceType, Piece


def test_piece_type():
    with pytest.raises(ValueError, match="invalid piece type value"):
        PieceType(-1)
    with pytest.raises(ValueError, match="invalid piece type char"):
        PieceType('X')

    type = PieceType(0)
    assert type != 'P'
    assert type == 0
    assert type == PieceType(0)
    assert hash(type) == hash(PieceType(0))
    assert repr(type) == "PieceType.PAWN"
    assert type.value == 0
    assert type.name == "PAWN"
    assert type.char == 'P'
    assert not type.sliding

    type = PieceType('B')
    assert type != 'B'
    assert type == 2
    assert type == PieceType('B')
    assert hash(type) == hash(PieceType('B'))
    assert repr(type) == "PieceType.BISHOP"
    assert type.value == 2
    assert type.name == "BISHOP"
    assert type.char == 'B'
    assert type.sliding

    assert len(list(PieceType)) == 6


def test_piece():
    with pytest.raises(ValueError, match="invalid piece arguments"):
        Piece()
    with pytest.raises(ValueError, match="invalid piece arguments"):
        Piece(0)
    with pytest.raises(ValueError, match="invalid piece char"):
        Piece('')
    with pytest.raises(ValueError, match="invalid piece arguments"):
        Piece(0, 0)
    with pytest.raises(ValueError, match="invalid piece arguments"):
        Piece(0, 0, 0)

    piece = Piece('K')
    assert repr(piece) == "Piece.WHITE_KING"
    assert piece.white is True
    assert piece.type == 5
    assert piece.name == "WHITE_KING"
    assert piece.char == 'K'

    piece = Piece(False, PieceType('N'))
    assert repr(piece) == "Piece.BLACK_KNIGHT"
    assert piece.white is False
    assert piece.type == 1
    assert piece.name == "BLACK_KNIGHT"
    assert piece.char == 'n'
