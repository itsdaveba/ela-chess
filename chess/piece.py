PAWN = 0
KNIGHT = 1
BISHOP = 2
ROOK = 3
QUEEN = 4
KING = 5

piece_name = {
    PAWN: "PAWN",
    KNIGHT: "KNIGHT",
    BISHOP: "BISHOP",
    ROOK: "ROOK",
    QUEEN: "QUEEN",
    KING: "KING"
}
color_name = ["BLACK", "WHITE"]


class PieceType:
    def __init__(self, val: int | str) -> None:
        self.value: int
        self.name: str
        self.char: str
        self.sliding: bool

        if isinstance(val, int):
            if val not in piece_name:
                raise ValueError(f"invalid piece type value: {val}")
            self.value = val

        else:
            if len(val) != 1 or val not in "PNBRQK":
                raise ValueError(f"invalid piece type char: '{val}'")
            self.value = "PNBRQK".index(val)

        self.name = piece_name[self.value]
        self.char = "N" if self.value == KNIGHT else self.name[0]
        self.sliding = self.char in "BRQ"

    def __repr__(self) -> str:
        return f"PieceType.{self.name}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PieceType):
            if isinstance(other, int):
                return self.value == other
            return False
        return self.value == other.value


class Piece:
    def __init__(self, *args) -> None:
        self.white: bool
        self.type: PieceType
        self.name: str
        self.char: str

        if len(args) == 1:
            piece_char = args[0]
            if not isinstance(piece_char, str):
                raise ValueError("invalid piece arguments")
            if len(piece_char) != 1:
                raise ValueError(f"invalid piece char: '{piece_char}'")
            self.white = piece_char.isupper()
            self.type = PieceType(piece_char.upper())
        elif len(args) == 2:
            color, type = args
            if not isinstance(color, bool) or not isinstance(type, PieceType):
                raise ValueError("invalid piece arguments")
            self.white = color
            self.type = type
        else:
            raise ValueError("invalid piece arguments")

        self.name = f"{color_name[self.white]}_{self.type.name}"
        self.char = self.type.char if self.white else self.type.char.lower()

    def __repr__(self) -> str:
        return f"Piece.{self.name}"
