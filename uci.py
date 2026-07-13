from chess import ChessGame, EnginePlayer


game = ChessGame()
engine = EnginePlayer()

while True:
    tokens = input().split()
    command = tokens[0]

    match command:
        case "uci":
            print("id name ElaChess")
            print("id author Dave Barragan")
            print("uciok")
        case "isready":
            print("readyok")
        case "ucinewgame":
            pass
        case "position":
            if tokens[1] == "startpos":
                index = 3
                game.reset()
            else:
                index = 9
                game.reset(" ".join(tokens[2:8]))
            for move in tokens[index:]:
                game.make_move(move)
        case "go":
            move = engine.best_move(game.position)
            print(f"bestmove {move}")
        case "quit":
            break
