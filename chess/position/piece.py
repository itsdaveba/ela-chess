from enum import Enum


class Piece(int, Enum):
    OFF = -2
    NONE = -1

    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

    @classmethod
    def from_char(cls, char: str) -> "Piece":
        try:
            return from_char[char]
        except KeyError:
            raise ValueError(f"invalid piece char: '{char}'")

    @property
    def char(self) -> str:
        return to_char[self]


to_char: str = "PNBRQK*."
from_char: dict[str, Piece] = {
    "P": Piece.PAWN,
    "N": Piece.KNIGHT,
    "B": Piece.BISHOP,
    "R": Piece.ROOK,
    "Q": Piece.QUEEN,
    "K": Piece.KING
}
