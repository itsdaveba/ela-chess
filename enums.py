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
        if self == Player.WHITE:
            return Player.BLACK
        if self == Player.BLACK:
            return Player.WHITE
        raise ValueError


class PieceType(Enum):
    NONE = 0

    KING = 1
    QUEEN = 2
    ROOK = 3
    BISHOP = 4
    KNIGHT = 5
    PAWN = 6

    @property
    def chr(self) -> str:
        if self == PieceType.NONE:
            return "."
        if self == PieceType.KNIGHT:
            return "N"
        return self.name[0]


# At the beginning of the game one player has 16 light-coloured pieces (the ‘white’ pieces);
# the other has 16 dark-coloured pieces (the ‘black’ pieces).
@dataclass
class PieceDataClass:
    player: Player
    type: PieceType


class Piece(PieceDataClass, Enum):
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

    @property
    def chr(self) -> str:
        ret = self.type.chr
        if self.player == Player.BLACK:
            ret = ret.lower()
        return ret
