from enum import Enum

# The game of chess is played between two opponents who move their pieces alternately on a square board called a ‘chessboard’.
player1 = "White"
player2 = "Black"


# At the beginning of the game one player has 16 light-coloured pieces (the ‘white’ pieces);
# the other has 16 dark-coloured pieces (the ‘black’ pieces).
class Piece(Enum):
    WHITE_KING = 1
    WHITE_QUEEN = 2
    WHITE_ROOK = 3
    WHITE_BISHOP = 4
    WHITE_KNIGHT = 5
    WHITE_PAWN = 6

    BLACK_KING = 7
    BLACK_QUEEN = 8
    BLACK_ROOK = 9
    BLACK_BISHOP = 10
    BLACK_KNIGHT = 11
    BLACK_PAWN = 12


# The chessboard is composed of an 8 x 8 grid of 64 equal squares.
# The initial position of the pieces on the chessboard is as follows:
board = [
    [Piece.BLACK_ROOK, Piece.BLACK_KNIGHT, Piece.BLACK_BISHOP, Piece.BLACK_QUEEN, Piece.BLACK_KING, Piece.BLACK_BISHOP, Piece.BLACK_KNIGHT, Piece.BLACK_ROOK],
    [Piece.BLACK_PAWN] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [None] * 8,
    [Piece.WHITE_PAWN] * 8,
    [Piece.WHITE_ROOK, Piece.WHITE_KNIGHT, Piece.WHITE_BISHOP, Piece.WHITE_QUEEN, Piece.WHITE_KING, Piece.WHITE_BISHOP, Piece.WHITE_KNIGHT, Piece.WHITE_ROOK]
]


def display_board(board):
    for rank in board:
        for square in rank:
            if square is None:
                print(".", end=" ")
                continue
            color, type = square.name.split("_")
            if color == "WHITE":
                if type == "KNIGHT":
                    print("N", end=" ")
                else:
                    print(type[0], end=" ")
            else:
                if type == "KNIGHT":
                    print("n", end=" ")
                else:
                    print(type[0].lower(), end=" ")
        print()


def make_move(board, move):
    pass


# The player with the white pieces commences the game.
turn = player1


# A player is said to ‘have the move’, when his opponent’s move has been ‘made’.
def have_the_move(turn):
    return turn


# The objective of each player is to place the opponent’s king ‘under attack’
def opponent_king_under_attack(board, turn) -> bool:
    return False


# in such a way that the opponent has no legal move.
def opponent_no_legal_move(board, turn) -> bool:
    return False


# Leaving one’s own king under attack
def own_king_under_attack(board, turn) -> bool:
    return False


# exposing one’s own king to attack
def exposing_own_king_to_attack(board, turn) -> bool:
    return False


# and also ’capturing’ the opponent’s king are not allowed.
def capturing_opponent_king(board, turn) -> bool:
    return False


# If the position is such that neither player can possibly checkmate, the game is drawn.
def no_possible_checkmate(board) -> bool:
    return False


# The opponent whose king has been checkmated has lost the game.
if __name__ == "__main__":
    while True:
        print("Turn:", have_the_move(turn))
        display_board(board)
        move = input("Move: ")
        make_move(board, move)
        if own_king_under_attack(board, turn):
            print("Cannot leave own king under attack")
            continue
        if exposing_own_king_to_attack(board, turn):
            print("Cannot expose own king to attack")
            continue
        if capturing_opponent_king(board, turn):
            print("Cannot capture opponent's king")
            continue
        if opponent_king_under_attack(board, turn):
            print("Oponent king under attack")
            if opponent_no_legal_move(board, turn):
                print("Opponent has no legal moves")
                # The player who achieves this goal is said to have ‘checkmated’ the opponent’s king and to have won the game.
                print("Checkmate")
                print("Winner:", turn)
                break
        if no_possible_checkmate(board):
            print("No possible to checkmate")
            print("Draw")
            break
        if turn == player1:
            turn = player2
        else:
            turn = player1
