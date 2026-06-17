from .square import Square
from .piece import PieceType, Piece

PAWN_MOVE = 1
PAWN_DOUBLE_MOVE = 2
PROMOTION = 4
CAPTURE = 8
EP_CAPTURE = 16
CASTLE = 32

order = ["PAWN_MOVE", "PAWN_DOUBLE_MOVE", "PROMOTION", "CAPTURE", "EP_CAPTURE", "CASTLE"]
flag_value = {
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
        return f"MoveType('{self.string}')"

    def __and__(self, other: int) -> int:
        return self.flags & other

    @property
    def string(self) -> str:
        string = [name for name in order if self.flags & flag_value[name]]

        if string:
            return "|".join(string)
        return "NORMAL_MOVE"


class Move:
    def __init__(self, *args) -> None:
        self.source: Square
        self.target: Square
        self.promotion: PieceType | None
        self.piece: Piece | None
        self.capture: Piece | None
        self.type: MoveType
        self.string: str

        if len(args) == 1:
            move_str = args[0]
            if not isinstance(move_str, str):
                raise ValueError("invalid move arguments")
            if len(move_str) not in (4, 5):
                raise ValueError(f"invalid move string: '{move_str}'")
            self.source = Square(move_str[:2])
            self.target = Square(move_str[2:4])
            self.promotion = None if len(move_str) == 4 else PieceType(move_str[4].upper())
            self.piece = None
            self.capture = None
            self.type = MoveType(0)
        elif len(args) == 5:
            from .board import Board
            source, target, board, flags, promotion = args
            if not isinstance(source, Square) or not isinstance(target, Square) or not isinstance(flags, int):
                raise ValueError("invalid move arguments")
            if not isinstance(board, Board):
                raise ValueError("invalid move arguments")
            if promotion is not None and not isinstance(promotion, (PieceType, int)):
                raise ValueError("invalid move arguments")
            self.source = source
            self.target = target
            self.promotion = promotion if (promotion is None or isinstance(promotion, PieceType)) else PieceType(promotion)
            self.piece = board[source]
            self.capture = board[target]
            self.type = MoveType(flags)
        else:
            raise ValueError("invalid move arguments")

        self.string = self.source.string + self.target.string + ('' if self.promotion is None else self.promotion.char.lower())

    def __repr__(self) -> str:
        return f"Move.{self.string.upper()}"

    def __str__(self) -> str:
        return self.string

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Move):
            if isinstance(other, str):
                return self.string == other.lower()
            return False
        return self.string == other.string
