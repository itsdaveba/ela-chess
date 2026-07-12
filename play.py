import argparse

from chess import ChessGame, Player, HumanPlayer, EnginePlayer

PLAYER: dict[str, type[Player]] = {
    "human": HumanPlayer,
    "engine": EnginePlayer
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("fen", nargs="?")
    parser.add_argument("-w", "--white", choices=["human", "engine"], default="human")
    parser.add_argument("-b", "--black", choices=["human", "engine"], default="engine")

    args = parser.parse_args()

    fen = args.fen
    white = PLAYER[args.white]()
    black = PLAYER[args.black]()

    game = ChessGame(white, black, fen)

    game.play()
