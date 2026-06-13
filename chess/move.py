from .square import Square
from .piece import PieceType

PAWN_MOVE = 1
PAWN_DOUBLE_MOVE = 2
PROMOTION = 4
CAPTURE = 8
EP_CAPTURE = 16
CASTLE = 32

order = ["PAWN_MOVE", "PAWN_DOUBLE_MOVE", "PROMOTION", "CAPTURE", "EP_CAPTURE", "CASTLE"]
flag = {
    "CASTLE": CASTLE,
    "EP_CAPTURE": EP_CAPTURE,
    "CAPTURE": CAPTURE,
    "PROMOTION": PROMOTION,
    "PAWN_DOUBLE_MOVE": PAWN_DOUBLE_MOVE,
    "PAWN_MOVE": PAWN_MOVE
}


class MoveType:
    def __init__(self, flags: int) -> None:
        self.flags: int

        if flags < 0 or flags >= 64:
            raise ValueError(f"invalid move type flags: {flags}")

        self.flags: int = flags

    def __repr__(self) -> str:
        return f"MoveType('{self.str}')"

    @property
    def str(self) -> str:
        string = [name for name in order if self.flags & flag[name]]

        if string:
            return "|".join(string)
        return "NORMAL_MOVE"


class Move:
    def __init__(self, *args) -> None:
        self.source: Square
        self.target: Square
        self.promotion: PieceType | None
        self.str: str

        if len(args) == 1:
            move_str = args[0]
            if not isinstance(move_str, str):
                raise ValueError(f"invalid move arguments")
            if len(move_str) not in (4, 5):
                raise ValueError(f"invalid move string: {move_str}")
            self.source = Square(move_str[:2])
            self.target = Square(move_str[2:4])
            self.promotion = None if len(move_str) == 4 else PieceType(move_str[4].upper())
        elif len(args) == 3:
            source, target, promotion = args
            if not isinstance(source, Square) or not isinstance(target, Square):
                raise ValueError("invalid move arguments")
            if promotion is not None and not isinstance(promotion, (PieceType, int)):
                raise ValueError("invalid move arguments")
            self.source = source
            self.target = target
            self.promotion = promotion if promotion is None or isinstance(promotion, PieceType) else PieceType(promotion)
        else:
            raise ValueError("invalid move arguments")

        self.str = self.source.str + self.target.str + ('' if self.promotion is None else self.promotion.char.lower())

    def __repr__(self) -> str:
        return f"Move.{self.str.upper()}"

    # @classmethod
    # def from_string(cls, string: str) -> "Move":
    #     if len(string) != 4:
    #         raise ValueError

    #     source, target = string[:2], string[2:]
    #     return cls(Square.from_string(source), Square.from_string(target), None, None)

    # def get_string(self) -> str:
    #     return self.source.get_string() + self.target.get_string()
