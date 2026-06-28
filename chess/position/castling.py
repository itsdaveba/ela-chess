from enum import IntFlag


class Castling(IntFlag):
    WHITE_KINGSIDE = 8
    WHITE_QUEENSIDE = 4
    BLACK_KINGSIDE = 2
    BLACK_QUEENSIDE = 1

    NONE = 0

    @classmethod
    def from_string(cls, string: str) -> "Castling":
        try:
            return Castling(from_string[string])
        except KeyError:
            raise ValueError(f"invalid castling string: '{string}'")

    @property
    def string(self) -> str:
        return to_string[self]


to_string: list[str] = ["-", "q", "k", "kq", "Q", "Qq", "Qk", "Qkq", "K", "Kq", "Kk", "Kkq", "KQ", "KQq", "KQk", "KQkq"]
from_string: dict[str, int] = {
    "-": 0,
    "q": 1,
    "k": 2,
    "kq": 3,
    "Q": 4,
    "Qq": 5,
    "Qk": 6,
    "Qkq": 7,
    "K": 8,
    "Kq": 9,
    "Kk": 10,
    "Kkq": 11,
    "KQ": 12,
    "KQq": 13,
    "KQk": 14,
    "KQkq": 15,
}
