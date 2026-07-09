from enum import Enum


class File(int, Enum):
    NONE = -1

    FA = 0
    FB = 1
    FC = 2
    FD = 3
    FE = 4
    FF = 5
    FG = 6
    FH = 7


class Rank(int, Enum):
    NONE = -1

    R8 = 0
    R7 = 1
    R6 = 2
    R5 = 3
    R4 = 4
    R3 = 5
    R2 = 6
    R1 = 7


class Square(int, Enum):
    NONE = -1

    A8 = 1
    B8 = 2
    C8 = 3
    D8 = 4
    E8 = 5
    F8 = 6
    G8 = 7
    H8 = 8

    A7 = 11
    B7 = 12
    C7 = 13
    D7 = 14
    E7 = 15
    F7 = 16
    G7 = 17
    H7 = 18

    A6 = 21
    B6 = 22
    C6 = 23
    D6 = 24
    E6 = 25
    F6 = 26
    G6 = 27
    H6 = 28

    A5 = 31
    B5 = 32
    C5 = 33
    D5 = 34
    E5 = 35
    F5 = 36
    G5 = 37
    H5 = 38

    A4 = 41
    B4 = 42
    C4 = 43
    D4 = 44
    E4 = 45
    F4 = 46
    G4 = 47
    H4 = 48

    A3 = 51
    B3 = 52
    C3 = 53
    D3 = 54
    E3 = 55
    F3 = 56
    G3 = 57
    H3 = 58

    A2 = 61
    B2 = 62
    C2 = 63
    D2 = 64
    E2 = 65
    F2 = 66
    G2 = 67
    H2 = 68

    A1 = 71
    B1 = 72
    C1 = 73
    D1 = 74
    E1 = 75
    F1 = 76
    G1 = 77
    H1 = 78

    @classmethod
    def from_string(cls, string: str) -> "Square":
        if string == "-":
            return Square.NONE
        if len(string) != 2:
            raise ValueError(f"invalid square string: '{string}'")
        try:
            return Square[string.upper()]
        except KeyError:
            raise ValueError(f"invalid square string: '{string}'")

    @property
    def string(self) -> str:
        return "-" if self == Square.NONE else self.name.lower()

    @property
    def file(self) -> File:
        return File.NONE if self == Square.NONE else File(self.value % 10 - 1)

    @property
    def rank(self) -> Rank:
        return Rank.NONE if self == Square.NONE else Rank(self.value // 10)
