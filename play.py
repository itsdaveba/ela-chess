import argparse

from chess import ChessGame


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--fen")
    parser.add_argument("--white", choices=["human", "engine"], default="human")
    parser.add_argument("--black", choices=["human", "engine"], default="engine")

    args = parser.parse_args()

    fen = args.fen
    wplayer = args.white
    bplayer = args.black

    game = ChessGame()
    game.play(fen, wplayer, bplayer)
