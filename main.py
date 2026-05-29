# The game of chess is played between two opponents who move their pieces alternately on a square board called a ‘chessboard’.
player1 = "White"
player2 = "Black"
board = None  # square board


def make_move(board, move):
    pass


# The player with the white pieces commences the game.
turn = player1


# A player is said to ‘have the move’, when his opponent’s move has been ‘made’.
def have_the_move():
    return turn


if __name__ == "__main__":
    while True:
        print("Turn:", have_the_move())
        move = input("Move: ")
        make_move(board, move)
        if turn == player1:
            turn = player2
        else:
            turn = player1
