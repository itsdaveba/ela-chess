from enums import Piece, Player


class Board:
    def __init__(self):
        # The chessboard is composed of an 8 x 8 grid of 64 equal squares.
        # The initial position of the pieces on the chessboard is as follows:
        self.board: list[list[Piece]] = [
            [Piece.BLACK_ROOK, Piece.BLACK_KNIGHT, Piece.BLACK_BISHOP, Piece.BLACK_QUEEN,
             Piece.BLACK_KING, Piece.BLACK_BISHOP, Piece.BLACK_KNIGHT, Piece.BLACK_ROOK],
            [Piece.BLACK_PAWN] * 8,
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [Piece.WHITE_PAWN] * 8,
            [Piece.WHITE_ROOK, Piece.WHITE_KNIGHT, Piece.WHITE_BISHOP, Piece.WHITE_QUEEN,
             Piece.WHITE_KING, Piece.WHITE_BISHOP, Piece.WHITE_KNIGHT, Piece.WHITE_ROOK]
        ]
        # The player with the white pieces commences the game.
        self.player: Player = Player.WHITE

    def __str__(self) -> str:
        return "\n".join([" ".join([piece.chr for piece in rank]) for rank in self.board])

    def make_move(self, move: str) -> bool:
        if self.own_king_under_attack(move):
            print("Cannot leave own king under attack")
            return False
        if self.exposing_own_king_to_attack(move):
            print("Cannot expose own king to attack")
            return False
        if self.capturing_opponent_king(move):
            print("Cannot capture opponent's king")
            return False
        self.player = self.player.opponent
        return True

    # The objective of each player is to place the opponent’s king ‘under attack’
    def king_under_attack(self) -> bool:
        # self.player under attack
        return False

    # in such a way that the opponent has no legal move.
    def no_legal_move(self) -> bool:
        # seylf.player no legal moves
        return False

    # Leaving one’s own king under attack
    def own_king_under_attack(self, move: str) -> bool:
        return False

    # exposing one’s own king to attack
    def exposing_own_king_to_attack(self, move: str) -> bool:
        return False

    # and also ’capturing’ the opponent’s king are not allowed.
    def capturing_opponent_king(self, move: str) -> bool:
        return False

    # If the position is such that neither player can possibly checkmate, the game is drawn.
    def no_possible_checkmate(self) -> bool:
        return False
