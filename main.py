from board import Board


if __name__ == "__main__":
    board = Board()
    while True:
        # A player is said to ‘have the move’, when his opponent’s move has been ‘made’.
        print("Turn:", board.player)
        print(board)
        move = input("Move: ")
        if not board.make_move(move):
            print("Invalid move")
            continue
        if board.king_under_attack():
            print(f"{board.player} king under attack")
            if board.no_legal_move():
                print(f"{board.player} has no legal moves")
                # The player who achieves this goal is said to have ‘checkmated’ the opponent’s king and to have won the game.
                # The opponent whose king has been checkmated has lost the game.
                print("Checkmate")
                print("Winner:", board.player.opponent)
                print("Loser:", board.player)
                break
        if board.no_possible_checkmate():
            print("No possible to checkmate")
            print("Draw")
            break
