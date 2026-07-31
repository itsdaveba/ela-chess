from enum import Enum


NUM_SQUARES = 64


class File(int, Enum):
    FA = 0
    FB = 1
    FC = 2
    FD = 3
    FE = 4
    FF = 5
    FG = 6
    FH = 7

    NONE = 8


class Rank(int, Enum):
    R8 = 0
    R7 = 1
    R6 = 2
    R5 = 3
    R4 = 4
    R3 = 5
    R2 = 6
    R1 = 7

    NONE = 8


class Square(int, Enum):
    A8 = 0
    B8 = 1
    C8 = 2
    D8 = 3
    E8 = 4
    F8 = 5
    G8 = 6
    H8 = 7

    A7 = 8
    B7 = 9
    C7 = 10
    D7 = 11
    E7 = 12
    F7 = 13
    G7 = 14
    H7 = 15

    A6 = 16
    B6 = 17
    C6 = 18
    D6 = 19
    E6 = 20
    F6 = 21
    G6 = 22
    H6 = 23

    A5 = 24
    B5 = 25
    C5 = 26
    D5 = 27
    E5 = 28
    F5 = 29
    G5 = 30
    H5 = 31

    A4 = 32
    B4 = 33
    C4 = 34
    D4 = 35
    E4 = 36
    F4 = 37
    G4 = 38
    H4 = 39

    A3 = 40
    B3 = 41
    C3 = 42
    D3 = 43
    E3 = 44
    F3 = 45
    G3 = 46
    H3 = 47

    A2 = 48
    B2 = 49
    C2 = 50
    D2 = 51
    E2 = 52
    F2 = 53
    G2 = 54
    H2 = 55

    A1 = 56
    B1 = 57
    C1 = 58
    D1 = 59
    E1 = 60
    F1 = 61
    G1 = 62
    H1 = 63

    NONE = 64

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
        return File.NONE if self == Square.NONE else File(self.value % 8)

    @property
    def rank(self) -> Rank:
        return Rank.NONE if self == Square.NONE else Rank(self.value // 8)
