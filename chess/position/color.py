from enum import Enum


class Color(int, Enum):
    WHITE = 0
    BLACK = 1

    NONE = 2

    @classmethod
    def from_char(cls, char: str) -> "Color":
        try:
            return from_char[char]
        except KeyError:
            raise ValueError(f"invalid color char: '{char}'")

    @property
    def char(self) -> str:
        return to_char[self]

    @property
    def opponent(self) -> "Color":
        return opponent[self]


opponent: list[Color] = [Color.BLACK, Color.WHITE, Color.NONE]
to_char: str = "wb-"
from_char: dict[str, Color] = {
    "w": Color.WHITE,
    "b": Color.BLACK
}
