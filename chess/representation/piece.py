from enum import Enum


class Piece(int, Enum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

    @classmethod
    def from_char(cls, char: str) -> "Piece":
        if len(char) != 1:
            raise ValueError(f"invalid piece char: '{char}'")

        try:
            return cls(to_char.index(char))
        except ValueError:
            raise ValueError(f"invalid piece char: '{char}'")

    def to_char(self) -> str:
        return to_char[self]


to_char: str = "PNBRQK"
