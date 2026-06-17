from chess import Move, History


def test_history():
    history = History()

    assert repr(history) == "History([])"
    history.append(Move("e2e4"), 15, None, 42, [])
    history.append(Move("e7e5"), 15, None, 42, [])
    assert repr(history) == "History([Move.E2E4, Move.E7E5])"

    assert len(history) == 2
    history.pop()
    assert len(history) == 1
    history.clear()
    assert len(history) == 0
