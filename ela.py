import sys
import threading

from chess import Engine, Position


if __name__ == "__main__":

    engine = Engine(uci=True)
    position = Position()

    for line in sys.stdin:

        line = line.split()
        command = line[0]

        match command:
            case "uci":
                sys.stdout.write("id name ElaChess\n")
                sys.stdout.write("id author Dave Barragan\n")

                sys.stdout.write("uciok\n")

                sys.stdout.flush()

            case "isready":
                sys.stdout.write("readyok\n")

                sys.stdout.flush()

            case "position":
                moves = []
                subcommand = line[1]

                if subcommand == "fen":
                    position.fen = " ".join(line[2:8])
                    moves = line[9:]
                elif subcommand == "startpos":
                    position.reset()
                    moves = line[3:]

                for move in moves:
                    position.make_move(move)

            case "go":
                subcommand = line[1] if line[1:] else "infinite"

                if subcommand == "depth":
                    threading.Thread(target=engine.search, args=[position, int(line[2])]).start()
                else:
                    threading.Thread(target=engine.search, args=[position, -1]).start()

            case "stop":
                pass

            case "quit":
                break
