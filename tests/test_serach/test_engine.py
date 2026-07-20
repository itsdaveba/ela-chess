from chess import EnginePlayer, Position, Move


def test_engine():
    engine = EnginePlayer()
    position = Position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    move = engine.best_move(position.copy(), -1, 1, -1)
    assert isinstance(move, Move)

    position.fen = "rnb1kbnr/pppp1ppp/8/4p1q1/4P2P/8/PPPP1PP1/RNBQKBNR w KQkq - 1 3"
    move = engine.best_move(position.copy(), -1, 2, -1)
    assert isinstance(move, Move)
    assert move.string == "h4g5"
    move = engine.best_move(position.copy(), 1000, -1, -1)
    assert isinstance(move, Move)
    assert move.string == "h4g5"
    move = engine.best_move(position.copy(), -1, -1, 1000)
    assert isinstance(move, Move)
    assert move.string == "h4g5"

    position.fen = "rnbqkbnr/ppppppp1/8/7p/4P1Q1/8/PPPP1PPP/RNB1KBNR b KQkq - 1 2"
    move = engine.best_move(position.copy(), -1, 2, -1)
    assert isinstance(move, Move)
    assert move.string == "h5g4"
    move = engine.best_move(position.copy(), 1000, -1, -1)
    assert isinstance(move, Move)
    assert move.string == "h5g4"
    move = engine.best_move(position.copy(), -1, -1, 1000)
    assert isinstance(move, Move)
    assert move.string == "h5g4"

    position.fen = "7k/5K2/1Q6/8/8/8/8/8 w - - 0 1"
    move = engine.best_move(position.copy(), -1, 2, -1)
    assert isinstance(move, Move)
    assert move.string == "b6h6"
    move = engine.best_move(position.copy(), 1000, -1, -1)
    assert isinstance(move, Move)
    assert move.string == "b6h6"
    move = engine.best_move(position.copy(), -1, -1, 10000)
    assert isinstance(move, Move)
    assert move.string == "b6h6"

    position.fen = "6k1/3R4/5K2/8/8/8/8/8 b - - 0 1"
    move = engine.best_move(position.copy(), -1, 5, -1)
    assert isinstance(move, Move)
    assert move.string == "g8h8"
    move = engine.best_move(position.copy(), 1000, -1, -1)
    assert isinstance(move, Move)
    assert move.string == "g8h8"
    move = engine.best_move(position.copy(), -1, -1, 10000)
    assert isinstance(move, Move)
    assert move.string == "g8h8"
