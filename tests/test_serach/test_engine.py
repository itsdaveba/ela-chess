from chess import EnginePlayer, Position, Move


def test_engine():
    engine = EnginePlayer()
    position = Position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    move = engine.best_move(position.copy(), -1, 1, -1)
    assert isinstance(move, Move)
