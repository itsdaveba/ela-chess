from enum import Enum


class Piece(int, Enum):
    NONE = 0

    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

    @classmethod
    def from_char(cls, char: str) -> "Piece":
        if len(char) != 1:
            raise ValueError(f"invalid piece char: '{char}'")

        try:
            return from_char[char]
        except KeyError:
            raise ValueError(f"invalid piece char: '{char}'")

    @property
    def char(self) -> str:
        return to_char[self]


to_char: str = ".PNBRQK"
from_char: dict[str, Piece] = {
    ".": Piece.NONE,
    "P": Piece.PAWN,
    "N": Piece.KNIGHT,
    "B": Piece.BISHOP,
    "R": Piece.ROOK,
    "Q": Piece.QUEEN,
    "K": Piece.KING
}
