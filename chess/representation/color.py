from enum import Enum


class Color(int, Enum):
    WHITE = 0
    BLACK = 1

    @classmethod
    def from_char(cls, char: str) -> "Color":
        if char == "w":
            return Color.WHITE
        elif char == "b":
            return Color.BLACK
        raise ValueError(f"invalid color char: '{char}'")

    @property
    def char(self) -> str:
        return "wb"[self]
