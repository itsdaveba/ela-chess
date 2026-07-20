import os
import io
from datetime import datetime

from chess import ChessGame, HumanPlayer, EnginePlayer


def test_game(monkeypatch, capsys):
    white = HumanPlayer()
    black = EnginePlayer()

    game = ChessGame()
    assert repr(game) == "ChessGame(white=None, black=None, result=None, history=[])"
    assert game.has_legal_moves()

    assert game.make_move("e2e4")
    assert repr(game) == "ChessGame(white=None, black=None, result=None, history=[Move.E2E4])"

    move = game.undo_move()
    assert move is not None
    assert move.string == "e2e4"
    assert repr(game) == "ChessGame(white=None, black=None, result=None, history=[])"

    move = game.undo_move()
    assert move is None
    captured = capsys.readouterr()
    assert captured.out.find("No previous move") != -1

    game = ChessGame("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 1")
    assert repr(game) == "ChessGame(fen='rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 1', \
white=None, black=None, result=None, history=[])"
    assert not game.has_legal_moves()
    assert not game.make_move("e2e4")

    game.play(white, black, -1, 1, -1)
    captured = capsys.readouterr()
    assert captured.out.find("Checkmate") != -1

    game.reset()
    assert repr(game) == "ChessGame(white=None, black=None, result=None, history=[])"
    assert str(game) == f"""\
[Event "?"]
[Site "Ela Chess"]
[Date "{datetime.today().strftime("%Y.%m.%d")}"]
[Round "?"]
[White "?"]
[Black "?"]
[Result "*"]

"""

    game = ChessGame("7k/5K2/8/6Q1/8/8/8/8 w - - 97 1")
    monkeypatch.setattr('sys.stdin', io.StringIO("g5g6"))
    game.play(white, black, -1, 1, -1)
    captured = capsys.readouterr()
    assert captured.out.find("Stalemate") != -1

    game.undo_move()
    monkeypatch.setattr('sys.stdin', io.StringIO("resign"))
    game.play(white, black, -1, 1, -1)
    captured = capsys.readouterr()
    assert captured.out.find("resigns") != -1

    monkeypatch.setattr('sys.stdin', io.StringIO("undo\nquit"))
    game.play(white, black, -1, 1, -1)
    captured = capsys.readouterr()
    assert captured.out.find("No previous move") != -1

    monkeypatch.setattr('sys.stdin', io.StringIO("x\nquit"))
    game.play(white, black, -1, 1, -1)
    captured = capsys.readouterr()
    assert captured.out.find("Invalid move: 'x'") != -1

    monkeypatch.setattr('sys.stdin', io.StringIO("e2e4\nquit"))
    game.play(white, black, -1, 1, -1)
    captured = capsys.readouterr()
    assert captured.out.find("Illegal move: 'e2e4'") != -1

    monkeypatch.setattr('sys.stdin', io.StringIO("f7g7\nquit"))
    game.play(white, black, -1, 1, -1)
    captured = capsys.readouterr()
    assert captured.out.find("Illegal move: 'f7g7'") != -1

    monkeypatch.setattr('sys.stdin', io.StringIO("g5g4\nundo\ng5g4\ng4h4"))
    game.play(white, black, -1, 1, -1)
    assert repr(game) == "ChessGame(fen='7k/5K2/8/6Q1/8/8/8/8 w - - 97 1', \
white=Human, black=Engine, result=Color.WHITE, history=[Move.G5G4, Move.H8H7, Move.G4H4])"
    assert str(game) == f"""\
[Event "Player vs Engine"]
[Site "Ela Chess"]
[Date "{datetime.today().strftime("%Y.%m.%d")}"]
[Round "?"]
[White "Player"]
[Black "ElaChess"]
[Result "1-0"]
[SetUp "1"]
[FEN "7k/5K2/8/6Q1/8/8/8/8 w - - 97 1"]

g5g4 h8h7 g4h4"""
    captured = capsys.readouterr()
    assert captured.out.find("Engine move: h8h7") != -1

    game.save_pgn()
    captured = capsys.readouterr()
    assert captured.out.find("PGN file saved") != -1
    filename = f"Player_vs_ElaChess_{datetime.today():%Y.%m.%d}.pgn"
    os.remove(filename)

    game.save_pgn("test.pgn")
    captured = capsys.readouterr()
    assert captured.out.find("PGN file saved: 'test.pgn'") != -1
    os.remove("test.pgn")

    game.display()
    captured = capsys.readouterr()
    assert captured.out.find("Black to move") != -1

    game.undo_move()
    monkeypatch.setattr('sys.stdin', io.StringIO("g4g5"))
    game.play(white, black, -1, 0, -1)
    captured = capsys.readouterr()
    assert captured.out.find("Fifty-move rule") != -1
