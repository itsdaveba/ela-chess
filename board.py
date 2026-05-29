import re
from enums import Piece, PieceType, Player
from dataclasses import dataclass


@dataclass
class Move:
    src: tuple[int, int]
    dst: tuple[int, int]
    parsed: bool

    def __init__(self, move_str):
        if re.match("^[0-7]{4}$", move_str) is None:
            self.parsed = False
            return
        self.parsed = True
        self.src = int(move_str[0]), int(move_str[1])
        self.dst = int(move_str[2]), int(move_str[3])


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

    def __getitem__(self, key: tuple[int, int]) -> Piece:
        return self.board[key[0]][key[1]]

    def __setitem__(self, key: tuple[int, int], value: Piece):
        self.board[key[0]][key[1]] = value

    def make_move(self, move: Move) -> bool:
        king_under_attack = self.king_under_attack()
        # It is not permitted to move a piece to a square occupied by a piece of the same colour.
        if self[move.dst].player == self.player:
            print("Not permitted to move to same color")
            return False
        # and also ’capturing’ the opponent’s king are not allowed.
        if self[move.dst].type == PieceType.KING:
            print("Cannot capture opponent's king")
            return False
        # who move their pieces alternately on a square board called a ‘chessboard’.
        if self[move.src].player != self.player:
            print(f"Player {self.player} needs to move its own piece")
            return False
        # If a piece moves to a square occupied by an opponent’s piece
        # the latter is captured and removed from the chessboard as part of the same move.
        captured_piece = self[move.dst]
        self[move.dst] = self[move.src]
        self[move.src] = Piece.NONE
        if self.king_under_attack():
            # Leaving one’s own king under attack
            if king_under_attack:
                print("Cannot leave own king under attack")
            # exposing one’s own king to attack
            else:
                print("Cannot expose own king to attack")
            self[move.src] = self[move.dst]
            self[move.dst] = captured_piece
            return False

        self.player = self.player.opponent
        return True

    # The objective of each player is to place the opponent’s king ‘under attack’
    def king_under_attack(self) -> bool:
        own_king = Piece((self.player, PieceType.KING))
        for opponent_piece_type in PieceType:
            opponent_piece = Piece((self.player.opponent, opponent_piece_type))
            if self.is_piece_attacked_by_opponent_piece(own_king, opponent_piece):
                return True
        return False

    # in such a way that the opponent has no legal move.
    def no_legal_move(self) -> bool:
        # seylf.player no legal moves
        return False

    # If the position is such that neither player can possibly checkmate, the game is drawn.
    def no_possible_checkmate(self) -> bool:
        return False

    # A piece is said to attack an opponent’s piece if the piece could make a capture on that square
    # according to the Articles 3.2 to 3.8.
    def is_piece_attacked_by_opponent_piece(self, piece: Piece, opponent_piece: Piece) -> bool:
        return False

    # A piece is considered to attack a square, even if such a piece is constrained from moving to that square
    # because it would then leave or place the king of its own colour under attack.
    def is_square_attacked_by_piece(self, square: tuple[int, int], piece: Piece) -> bool:
        return False
