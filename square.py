from __future__ import annotations

from enums import Direction


class Square:
    def __init__(self, rank: int, file: int) -> None:
        self.rank = rank
        self.file = file

    def __repr__(self) -> str:
        return f"({self.rank}, {self.file})"

    def __add__(self, direction: Direction) -> Square:
        return Square(self.rank + direction.rank_diff, self.file + direction.file_diff)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Square):
            return False
        return self.rank == other.rank and self.file == other.file

    def __gt__(self, value: int) -> bool:
        return self.rank > value and self.file > value

    def __ge__(self, value: int) -> bool:
        return self.rank >= value and self.file >= value

    def __lt__(self, value: int) -> bool:
        return self.rank < value and self.file < value

    def __le__(self, value: int) -> bool:
        return self.rank <= value and self.file <= value
