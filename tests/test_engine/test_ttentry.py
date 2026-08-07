from chess import TTEntry, MoveType, NodeType


def test_ttentry():
    ttentry = TTEntry.null()
    assert ttentry.hash == 0
    assert ttentry.best.type == MoveType.NONE
    assert ttentry.depth == 0
    assert ttentry.score == 0
    assert ttentry.type == NodeType.NONE


def test_type():
    assert len(NodeType) == 4
    assert NodeType.NONE
