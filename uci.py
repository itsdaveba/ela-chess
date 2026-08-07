import sys
from threading import Thread
from time import perf_counter

from chess import ChessGame, EnginePlayer, perft
from chess.engine.engine import MIN_HASH_SIZE, MAX_HASH_SIZE, DEFAULT_HASH_SIZE


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
                sys.stdout.write("id name ElaChess 0.5\n")
                sys.stdout.write("id author Dave Barragan\n")
                sys.stdout.write(f"option name Hash type spin default {DEFAULT_HASH_SIZE} ")
                sys.stdout.write(f"min {MIN_HASH_SIZE} max {MAX_HASH_SIZE}\n")
                sys.stdout.write("uciok\n")
                sys.stdout.flush()

            case "setoption":
                name = " ".join(tokens[2:])
                try:
                    if tokens[2] == "Hash":
                        value = int(tokens[4])
                        if value < MIN_HASH_SIZE or value > MAX_HASH_SIZE:
                            raise Exception
                        engine.hash_size = value
                    else:
                        raise Exception
                except Exception:
                    sys.stdout.write(f"No such option: '{name}'\n")
                    sys.stdout.flush()

            case "isready":
                sys.stdout.write("readyok\n")
                sys.stdout.flush()

            case "ucinewgame":
                engine.reset()

            case "position":
                try:
                    param = tokens[1]
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
                            continue
                    if index:
                        for move in tokens[index:]:
                            if not game.make_move(move):
                                break
                except Exception:
                    pass

            case "go":
                time = depth = nodes = -1

                try:
                    subcommand = tokens[1]

                    if subcommand == "perft":
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
                        time = int(tokens[2])
                    elif subcommand == "depth":
                        depth = int(tokens[2])
                    elif subcommand == "nodes":
                        nodes = int(tokens[2])
                    else:
                        t = [int(tokens[tokens.index("wtime") + 1]), int(tokens[tokens.index("btime") + 1])]
                        inc = [int(tokens[tokens.index("winc") + 1]), int(tokens[tokens.index("binc") + 1])]
                        time = int(t[game.side] / 20 + inc[game.side] / 2)
                except Exception:
                    pass

                search_thread = Thread(target=search, args=(engine, game, time, depth, nodes, True))
                search_thread.start()

            case "stop":
                if search_thread.is_alive():
                    engine.stop = True
                    search_thread.join()
                    sys.stdout.write(f"bestmove {engine.best_move}\n")
                    sys.stdout.flush()

            case "d":
                sys.stdout.write(f"{game.position}\n")
                sys.stdout.write(f"FEN: {game.position.fen}\n")
                sys.stdout.flush()

            case "eval":
                sys.stdout.write(f"{game.eval / 100:+.2f} (white side)\n")
                sys.stdout.flush()

            case "quit":
                if search_thread.is_alive():
                    engine.stop = True
                    search_thread.join()
                break

            case _:
                sys.stdout.write(f"Unknown command: '{command}'\n")
                sys.stdout.flush()
