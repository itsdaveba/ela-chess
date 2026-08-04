from threading import Thread

from chess import EnginePlayer, ChessGame, Move


def test_engine(capsys):
    engine = EnginePlayer()
    game = ChessGame()
    move = engine.search(game, -1, 1, -1)
    assert isinstance(move, Move)

    game.reset("rnb1kbnr/pppp1ppp/8/4p1q1/4P2P/8/PPPP1PP1/RNBQKBNR w KQkq - 1 3")
    move = engine.search(game, -1, 2, -1)
    assert isinstance(move, Move)
    assert move.string == "h4g5"
    game.reset("rnb1kbnr/pppp1ppp/8/4p1q1/4P2P/8/PPPP1PP1/RNBQKBNR w KQkq - 1 3")
    move = engine.search(game, 1000, -1, -1)
    assert isinstance(move, Move)
    assert move.string == "h4g5"
    game.reset("rnb1kbnr/pppp1ppp/8/4p1q1/4P2P/8/PPPP1PP1/RNBQKBNR w KQkq - 1 3")
    move = engine.search(game, -1, -1, 1000)
    assert isinstance(move, Move)
    assert move.string == "h4g5"

    game.reset("rnbqkbnr/ppppppp1/8/7p/4P1Q1/8/PPPP1PPP/RNB1KBNR b KQkq - 1 2")
    move = engine.search(game, -1, 2, -1)
    assert isinstance(move, Move)
    assert move.string == "h5g4"
    game.reset("rnbqkbnr/ppppppp1/8/7p/4P1Q1/8/PPPP1PPP/RNB1KBNR b KQkq - 1 2")
    move = engine.search(game, 1000, -1, -1)
    assert isinstance(move, Move)
    assert move.string == "h5g4"
    game.reset("rnbqkbnr/ppppppp1/8/7p/4P1Q1/8/PPPP1PPP/RNB1KBNR b KQkq - 1 2")
    move = engine.search(game, -1, -1, 1000)
    assert isinstance(move, Move)
    assert move.string == "h5g4"

    game.reset("7k/5K2/1Q6/8/8/8/8/8 w - - 0 1")
    move = engine.search(game, -1, 2, -1, True)
    captured = capsys.readouterr()
    assert captured.out.find("info depth 1 score cp") != -1
    assert captured.out.find("info depth 2 score mate 1") != -1
    assert isinstance(move, Move)
    assert move.string == "b6h6"
    game.reset("7k/5K2/1Q6/8/8/8/8/8 w - - 0 1")
    move = engine.search(game, 1000, -1, -1)
    assert isinstance(move, Move)
    assert move.string == "b6h6"
    game.reset("7k/5K2/1Q6/8/8/8/8/8 w - - 0 1")
    move = engine.search(game, -1, -1, 10000)
    assert isinstance(move, Move)
    assert move.string == "b6h6"

    game.reset("6k1/3R4/5K2/8/8/8/8/8 b - - 0 1")
    move = engine.search(game, -1, 5, -1, True)
    captured = capsys.readouterr()
    assert captured.out.find("info depth 1 score cp") != -1
    assert captured.out.find("info depth 5 score mate -2") != -1
    assert isinstance(move, Move)
    assert move.string == "g8h8"
    game.reset("6k1/3R4/5K2/8/8/8/8/8 b - - 0 1")
    move = engine.search(game, 1000, -1, -1)
    assert isinstance(move, Move)
    assert move.string == "g8h8"
    game.reset("6k1/3R4/5K2/8/8/8/8/8 b - - 0 1")
    move = engine.search(game, -1, -1, 10000)
    assert isinstance(move, Move)
    assert move.string == "g8h8"

    game.reset("rkn5/ppp5/8/8/8/8/5q2/1R5K w - - 0 1")
    move = engine.search(game, -1, 3, -1, True)
    captured = capsys.readouterr()
    assert captured.out.find("info depth 3 score cp 0") != -1
    assert isinstance(move, Move)
    assert move.string == "b1b7"
    game.reset("rkn5/ppp5/8/8/8/8/5q2/1R5K w - - 0 1")
    move = engine.search(game, 1000, -1, -1)
    assert isinstance(move, Move)
    assert move.string == "b1b7"
    game.reset("rkn5/ppp5/8/8/8/8/5q2/1R5K w - - 0 1")
    move = engine.search(game, -1, -1, 10000)
    assert isinstance(move, Move)
    assert move.string == "b1b7"

    game.reset("4k3/8/8/8/8/4P3/8/3QK3 w - - 99 1")
    move = engine.search(game, -1, 3, -1)
    assert isinstance(move, Move)
    assert move.string == "e3e4"
    game.reset("4k3/8/8/8/8/4P3/8/3QK3 w - - 99 1")
    move = engine.search(game, 1000, -1, -1)
    assert isinstance(move, Move)
    assert move.string == "e3e4"
    game.reset("4k3/8/8/8/8/4P3/8/3QK3 w - - 99 1")
    move = engine.search(game, -1, -1, 10000)
    assert isinstance(move, Move)
    assert move.string == "e3e4"

    game.reset("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3")
    move = engine.search(game, -1, -1, -1, True)
    captured = capsys.readouterr()
    assert captured.out.find("info depth 0 score mate 0") != -1
    assert isinstance(move, Move)
    assert move.string == "(none)"
    move = engine.search(game, -1, -1, -1)
    assert isinstance(move, Move)
    assert move.string == "(none)"

    game.reset("8/8/8/4k3/8/8/5q2/7K w - - 0 1")
    move = engine.search(game, -1, -1, -1, True)
    captured = capsys.readouterr()
    assert captured.out.find("info depth 0 score cp 0") != -1
    assert isinstance(move, Move)
    assert move.string == "(none)"

    # thread
    game.reset("6k1/3R4/5K2/8/8/8/8/8 b - - 0 1")
    thread = Thread(target=engine.search, args=(game, -1, -1, -1))
    thread.start()
    engine.stop = True
    thread.join()
    assert not thread.is_alive()
    assert isinstance(engine.best_move, Move)
    assert engine.best_move.string == "g8h8"
