from __future__ import annotations

from enum import Enum
from dataclasses import dataclass


# The game of chess is played between two opponents
class Player(Enum):
    NONE = 0

    WHITE = 1
    BLACK = 2

    @property
    def opponent(self) -> Player:
        if self is Player.WHITE:
            return Player.BLACK
        if self is Player.BLACK:
            return Player.WHITE
        raise ValueError


class PieceType(Enum):
    NONE = ".", False

    KING = "K", False
    QUEEN = "Q", True
    ROOK = "R", True
    BISHOP = "B", True
    KNIGHT = "N", False
    PAWN = "P", False

    def __init__(self, chr: str, is_sliding: bool):
        self.chr = chr
        self.is_sliding = is_sliding


# At the beginning of the game one player has 16 light-coloured pieces (the ‘white’ pieces);
# the other has 16 dark-coloured pieces (the ‘black’ pieces).
# TODO add move_type?
class Piece(Enum):
    NONE = Player.NONE, PieceType.NONE

    WHITE_KING = Player.WHITE, PieceType.KING
    WHITE_QUEEN = Player.WHITE, PieceType.QUEEN
    WHITE_ROOK = Player.WHITE, PieceType.ROOK
    WHITE_BISHOP = Player.WHITE, PieceType.BISHOP
    WHITE_KNIGHT = Player.WHITE, PieceType.KNIGHT
    WHITE_PAWN = Player.WHITE, PieceType.PAWN

    BLACK_KING = Player.BLACK, PieceType.KING
    BLACK_QUEEN = Player.BLACK, PieceType.QUEEN
    BLACK_ROOK = Player.BLACK, PieceType.ROOK
    BLACK_BISHOP = Player.BLACK, PieceType.BISHOP
    BLACK_KNIGHT = Player.BLACK, PieceType.KNIGHT
    BLACK_PAWN = Player.BLACK, PieceType.PAWN

    def __init__(self, player: Player, type: PieceType) -> None:
        self.player = player
        self.type = type
        self.chr = type.chr if player is Player.WHITE else type.chr.lower()


# The eight vertical columns of squares are called ‘files’.
class File(int, Enum):
    F0 = 0
    F1 = 1
    F2 = 2
    F3 = 3
    F4 = 4
    F5 = 5
    F6 = 6
    F7 = 7


#  The eight horizontal rows of squares are called ‘ranks’.
class Rank(int, Enum):
    R0 = 0
    R1 = 1
    R2 = 2
    R3 = 3
    R4 = 4
    R5 = 5
    R6 = 6
    R7 = 7


# A straight line of squares of the same colour,
# running from one edge of the board to an adjacent edge, is called a ‘diagonal’.


class Direction(Enum):
    UP = -1, 0
    DOWN = 1, 0
    RIGHT = 0, 1
    LEFT = 0, -1

    UP_RIGHT = -1, 1
    UP_LEFT = -1, -1
    DOWN_RIGHT = 1, 1
    DOWN_LEFT = 1, -1

    UP_UP_RIGHT = -2, 1
    UP_UP_LEFT = -2, -1
    RIGHT_RIGHT_UP = -1, 2
    LEFT_LEFT_UP = -1, -2
    RIGHT_RIGHT_DOWN = 1, 2
    LEFT_LEFT_DOWN = 1, -2
    DOWN_DOWN_RIGHT = 2, 1
    DOWN_DOWN_LEFT = 2, -1

    def __init__(self, rank_offset: int, file_offset: int) -> None:
        self.rank_offset = rank_offset
        self.file_offset = file_offset


@dataclass
class Move:
    source: Square
    target: Square
    promotion: PieceType


@dataclass(frozen=True)
class Square:
    rank: int
    file: int

    def __add__(self, offset: Direction) -> Square:
        return Square(self.rank + offset.rank_offset, self.file + offset.file_offset)

    def is_valid(self) -> bool:
        return Rank.R0 <= self.rank <= Rank.R7 and File.F0 <= self.file <= File.F7
