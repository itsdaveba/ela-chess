import sys
from threading import Thread
from time import perf_counter

from chess import ChessGame, EnginePlayer, perft


TIME_IDX = [2, 4]
INCR_IDX = [6, 8]


def search(engine: EnginePlayer, *args) -> None:
    best_move = engine.search(*args)
    if not engine.stop:
        sys.stdout.write(f"bestmove {best_move}\n")
        sys.stdout.flush()


if __name__ == "__main__":
    game = ChessGame()
    engine = EnginePlayer()
    search_thread = Thread()

    for line in sys.stdin:
        tokens = line.split()
        command = tokens[0]

        match command:
            case "uci":
                sys.stdout.write("id name ElaChess 0.3\n")
                sys.stdout.write("id author Dave Barragan\n")
                sys.stdout.write("uciok\n")
                sys.stdout.flush()

            case "setoption":
                name = tokens[2] if len(tokens) >= 3 else ""
                sys.stdout.write(f"No such option: '{name}'\n")
                sys.stdout.flush()

            case "isready":
                sys.stdout.write("readyok\n")
                sys.stdout.flush()

            case "ucinewgame":
                pass

            case "position":
                param = tokens[1] if len(tokens) >= 2 else ""
                index = 0
                if param == "startpos":
                    index = 3
                    game.reset()
                elif param == "fen":
                    index = 9
                    fen = " ".join(tokens[2:8])
                    try:
                        game.reset(fen)
                    except ValueError:
                        sys.stdout.write(f"Invalid fen: '{fen}'\n")
                        sys.stdout.flush()
                        continue
                if index:
                    for move in tokens[index:]:
                        if not game.make_move(move):
                            sys.stdout.write(f"Invalid move: '{move}'\n")
                            sys.stdout.flush()
                            break

            case "go":
                time = depth = nodes = -1
                subcommand = tokens[1] if len(tokens) >= 2 else "infinite"

                if subcommand == "perft":
                    if len(tokens) >= 3:
                        depth = int(tokens[2])
                        start_time = perf_counter()
                        nodes = perft(game.position, depth)
                        time_elapsed = perf_counter() - start_time
                        info = {
                            "depth": depth,
                            "nodes": nodes,
                            "nps": int(nodes / time_elapsed),
                            "time": int(time_elapsed * 1000)
                        }
                        sys.stdout.write("info")
                        for key in ["depth", "nodes", "nps", "time"]:
                            sys.stdout.write(f" {key} {info[key]}")
                        sys.stdout.write("\n")
                        sys.stdout.flush()
                        continue

                if subcommand == "movetime":
                    if len(tokens) >= 3:
                        time = int(tokens[2])
                elif subcommand == "depth":
                    if len(tokens) >= 3:
                        depth = int(tokens[2])
                elif subcommand == "nodes":
                    if len(tokens) >= 3:
                        nodes = int(tokens[2])
                elif subcommand == "wtime":
                    if len(tokens) >= 9:
                        side = game.position.side
                        time = int(int(tokens[TIME_IDX[side]]) / 20 + int(tokens[INCR_IDX[side]]) / 2)

                search_thread = Thread(target=search, args=(engine, game.position.copy(), time, depth, nodes, True))
                search_thread.start()

            case "stop":
                if search_thread.is_alive():
                    engine.stop = True
                    search_thread.join()
                    sys.stdout.write(f"bestmove {engine.best_move}\n")
                    sys.stdout.flush()

            case "d":
                sys.stdout.write(f"{game.position}\n")
                sys.stdout.flush()

            case "eval":
                sys.stdout.write(f"{game.position.eval / 100:+.2f} (white side)\n")
                sys.stdout.flush()

            case "quit":
                if search_thread.is_alive():
                    engine.stop = True
                    search_thread.join()
                break

            case _:
                sys.stdout.write(f"Unknown command: '{command}'\n")
                sys.stdout.flush()
