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

    counter_copy = counter.copy()
    assert counter_copy.value == counter.value

    counter.incr()
    assert counter.value == 2

    counter.decr()
    assert counter.value == 1

    counter.reset()
    assert counter.value == 0
