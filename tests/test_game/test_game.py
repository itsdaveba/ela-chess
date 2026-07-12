import io
import pytest

from chess import ChessGame, HumanPlayer, EnginePlayer, Move


def test_game(monkeypatch, capsys):
    white = HumanPlayer()
    black = EnginePlayer()

    game = ChessGame(white, black)
    assert repr(game) == "ChessGame(white='human', black='engine', history=[])"
    assert game.has_legal_moves()

    assert game.make_move(Move.from_string("e2e4"))
    assert repr(game) == "ChessGame(white='human', black='engine', history=[Move.E2E4])"

    game.undo_move()
    assert repr(game) == "ChessGame(white='human', black='engine', history=[])"

    with pytest.raises(ValueError, match="no previous move"):
        game.undo_move()

    game = ChessGame(white, black, "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 1")
    assert repr(game) == "ChessGame(white='human', black='engine', \
fen='rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 0 1', history=[])"
    assert not game.has_legal_moves()
    assert not game.make_move(Move.from_string("e2e4"))

    game.play()
    captured = capsys.readouterr()
    assert captured.out.find("Checkmate") != -1

    game.reset()
    assert repr(game) == "ChessGame(white='human', black='engine', history=[])"

    game = ChessGame(white, black, "7k/5K2/8/6Q1/8/8/8/8 w - - 0 1")
    monkeypatch.setattr('sys.stdin', io.StringIO("g5g6"))
    game.play()
    captured = capsys.readouterr()
    assert captured.out.find("Stalemate") != -1

    game.undo_move()
    monkeypatch.setattr('sys.stdin', io.StringIO("resign"))
    game.play()
    captured = capsys.readouterr()
    assert captured.out.find("resigns") != -1

    monkeypatch.setattr('sys.stdin', io.StringIO("undo\nquit"))
    game.play()
    captured = capsys.readouterr()
    assert captured.out.find("No previous move") != -1

    monkeypatch.setattr('sys.stdin', io.StringIO("x\nquit"))
    game.play()
    captured = capsys.readouterr()
    assert captured.out.find("Invalid move: 'x'") != -1

    monkeypatch.setattr('sys.stdin', io.StringIO("e2e4\nquit"))
    game.play()
    captured = capsys.readouterr()
    assert captured.out.find("Illegal move: 'e2e4'") != -1

    monkeypatch.setattr('sys.stdin', io.StringIO("f7g7\nquit"))
    game.play()
    captured = capsys.readouterr()
    assert captured.out.find("Illegal move: 'f7g7'") != -1

    monkeypatch.setattr('sys.stdin', io.StringIO("g5g4\nundo\ng5g4\ng4h4"))
    game.play()
    captured = capsys.readouterr()
    assert captured.out.find("Engine move: h8h7") != -1
