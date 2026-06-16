import pytest

from chess import Square, File, Rank


def test_file():
    with pytest.raises(ValueError, match="invalid file value"):
        File(-1)
    with pytest.raises(ValueError, match="invalid file char"):
        File('x')

    file = File(0)
    assert file != []
    assert file == 'a'
    assert repr(file) == "File.A"
    assert file.value == 0
    assert file.char == 'a'

    file = File('h')
    assert file != []
    assert file == 'h'
    assert repr(file) == "File.H"
    assert file.value == 7
    assert file.char == 'h'

    assert len(list(File)) == 8


def test_rank():
    with pytest.raises(ValueError, match="invalid rank value"):
        Rank(-1)
    with pytest.raises(ValueError, match="invalid rank char"):
        Rank('x')

    rank = Rank(0)
    assert rank != []
    assert rank == '8'
    assert rank == Rank(0)
    assert repr(rank) == "Rank.8"
    assert rank.value == 0
    assert rank.char == '8'

    rank = Rank('1')
    assert rank != []
    assert rank == '1'
    assert rank == Rank('1')
    assert repr(rank) == "Rank.1"
    assert rank.value == 7
    assert rank.char == '1'

    assert len(list(Rank)) == 8


def test_square():
    with pytest.raises(ValueError, match="invalid square arguments"):
        Square()
    with pytest.raises(ValueError, match="invalid square arguments"):
        Square(0)
    with pytest.raises(ValueError, match="invalid square string"):
        Square('x')
    with pytest.raises(ValueError, match="invalid square arguments"):
        Square(0, 0)
    with pytest.raises(ValueError, match="invalid square arguments"):
        Square(0, 0, 0)

    square = Square("e2")
    assert square == "e2"
    assert square == Square("e2")
    assert hash(square) == hash(Square("e2"))
    assert repr(square) == "Square.E2"
    assert square.file == File('e')
    assert square.rank == Rank('2')
    assert square.string == "e2"
    assert square + (1, 1) == Square("f1")

    square = Square(File('d'), Rank('5'))
    assert square != File('d'), Rank('5')
    assert square == Square(File('d'), Rank('5'))
    assert hash(square) == hash(Square(File('d'), Rank('5')))
    assert repr(square) == "Square.D5"
    assert square.file == File('d')
    assert square.rank == Rank('5')
    assert square.string == "d5"
    assert square + (-1, -1) == Square("c6")

    assert len(list(Square)) == 64
