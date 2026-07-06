import pytest

from chess import Counter


def test_counter():
    counter = Counter(0)
    assert repr(counter) == "Counter(0)"
    assert counter.string == "0"

    with pytest.raises(ValueError, match="invalid counter string"):
        Counter.from_string("-1")

    counter = Counter.from_string("1")
    assert repr(counter) == "Counter(1)"
    assert counter.string == "1"
