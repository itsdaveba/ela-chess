from enum import IntFlag
from dataclasses import dataclass

from ..position.piece import Piece
from ..position.square import Square


class MoveType(IntFlag):
    PAWN_MOVE = 32
    PAWN_DOUBLE_MOVE = 16
    PROMOTION = 8
    EPCAPTURE = 4
    CAPTURE = 2
    CASTLE = 1

    NONE = 0


@dataclass
class Move:
    source: Square
    target: Square
    piece: Piece
    type: MoveType
    promotion: Piece = Piece.NONE

    def __repr__(self) -> str:
        return f"Move.{self.string.upper()}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Move):
            return False

        if self.source != other.source:
            return False
        if self.target != other.target:
            return False
        if self.promotion != other.promotion:
            return False

        return True

    @classmethod
    def from_string(cls, string: str) -> "Move":
        if len(string) in (4, 5):
            source = Square.from_string(string[0:2])
            target = Square.from_string(string[2:4])
            promotion = Piece.NONE if len(string) == 4 else Piece.from_char(string[4].upper())
            return cls(source, target, Piece.NONE, MoveType.NONE, promotion)
        raise ValueError(f"invalid move string: '{string}'")

    @property
    def string(self) -> str:
        string = self.source.string + self.target.string
        if self.promotion != Piece.NONE:
            string += self.promotion.char.lower()
        return string
