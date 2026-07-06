from enum import Enum


class Color(int, Enum):
    NONE = -1

    WHITE = 0
    BLACK = 1

    @classmethod
    def from_char(cls, char: str) -> "Color":
        try:
            return from_char[char]
        except KeyError:
            raise ValueError(f"invalid color char: '{char}'")

    @property
    def char(self) -> str:
        return to_char[self]


to_char = "wb-"
from_char: dict[str, Color] = {
    "w": Color.WHITE,
    "b": Color.BLACK
}
