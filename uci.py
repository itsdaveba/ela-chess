from chess import ChessGame, EnginePlayer


TIME_IDX = [2, 4]
INC_IDX = [6, 8]


if __name__ == "__main__":
    game = ChessGame()
    engine = EnginePlayer()

    while True:
        tokens = input().split()
        command = tokens[0]

        match command:
            case "uci":
                print("id name ElaChess 0.2")
                print("id author Dave Barragan")
                print("uciok")

            case "setoption":
                name = tokens[2] if len(tokens) >= 3 else ""
                print(f"No such option: {name}")

            case "isready":
                print("readyok")

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
                    game.reset(" ".join(tokens[2:8]))
                if index:
                    for move in tokens[index:]:
                        game.make_move(move)

            case "go":
                time = depth = nodes = -1
                subcommand = tokens[1] if len(tokens) >= 2 else "infinite"

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
                        time = int(int(tokens[TIME_IDX[side]]) / 20 + int(tokens[INC_IDX[side]]) / 2)

                move = engine.best_move(game.position.copy(), time, depth, nodes)
                print(f"bestmove {move}")

            case "d":
                print(game.position)

            case "quit":
                break

            case _:
                print(f"Unknown command: '{command}'")
