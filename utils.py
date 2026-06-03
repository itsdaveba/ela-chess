import re

from defs import Move, Square, PieceType

chr_type: dict[str, PieceType] = {
    "q": PieceType.QUEEN,
    "r": PieceType.ROOK,
    "b": PieceType.BISHOP,
    "n": PieceType.KNIGHT
}


def parse_move(move: str) -> Move | None:
    if re.fullmatch("[0-7]{4}[qrbn]?", move) is None:
        return
    source = Square(int(move[0]), int(move[1]))
    target = Square(int(move[2]), int(move[3]))
    promotion = chr_type[move[-1]] if move[-1] in chr_type else PieceType.NONE
    return Move(source, target, promotion)
