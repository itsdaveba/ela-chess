import argparse

from chess import ChessGame, Player, HumanPlayer, EnginePlayer

PLAYER: dict[str, type[Player]] = {
    "human": HumanPlayer,
    "engine": EnginePlayer
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("fen", nargs="?")
    parser.add_argument("-w", "--white", choices=["human", "engine"], default="human", help="(default: human)")
    parser.add_argument("-b", "--black", choices=["human", "engine"], default="engine", help="(default: engine)")
    parser.add_argument("-t", "--time", type=int, default=-1)
    parser.add_argument("-d", "--depth", type=int, default=-1)
    parser.add_argument("-n", "--nodes", type=int, default=-1)
    parser.add_argument("-s", "--save", nargs="?", const="game.pgn", default=None)

    args = parser.parse_args()

    fen = args.fen
    white = PLAYER[args.white]()
    black = PLAYER[args.black]()
    time = args.time
    depth = args.depth
    nodes = args.nodes
    filename = args.save

    if time == -1 and depth == -1 and nodes == -1:
        parser.error("at least one of -t, -d, or -n must be specified")

    game = ChessGame(fen)
    game.play(white, black, time, depth, nodes)

    if filename is not None:
        game.save_pgn(filename)
        print()
