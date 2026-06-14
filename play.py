import sys

from chess import ChessGame


if __name__ == "__main__":
    game = ChessGame()

    if len(sys.argv) > 2:
        raise ValueError("too many arguments")

    fen = sys.argv[1]
    game.play(fen)
