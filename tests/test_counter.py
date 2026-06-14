import pytest

from chess import Counter


def test_counter():
    with pytest.raises(ValueError, match="invalid counter start"):
        Counter(-1)
    with pytest.raises(ValueError, match="invalid counter start"):
        Counter('')

    counter = Counter(0)
    assert repr(counter) == "Counter(0)"
    assert counter.start == 0
    assert counter.value == 0
    assert counter.string == "0"

    counter.next()
    assert repr(counter) == "Counter(1)"
    assert counter.start == 0
    assert counter.value == 1
    assert counter.string == "1"

    counter = Counter("1")
    assert repr(counter) == "Counter(1)"
    assert counter.start == 1
    assert counter.value == 1
    assert counter.string == "1"

    counter.prev()
    assert repr(counter) == "Counter(0)"
    assert counter.start == 1
    assert counter.value == 0
    assert counter.string == "0"

    counter.reset()
    assert repr(counter) == "Counter(1)"
    assert counter.start == 1
    assert counter.value == 1
    assert counter.string == "1"
