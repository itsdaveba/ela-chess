from enum import IntFlag


class Castling(IntFlag):
    pass

    @classmethod
    def from_string(cls, string: str) -> "Castling":
        return Castling(0)

    @property
    def string(self) -> str:
        return ""
