import re

from defs import Move, Square


def parse_move(move: str) -> Move | None:
    if re.fullmatch("[0-7]{4}", move) is None:
        return
    src = Square(int(move[0]), int(move[1]))
    dst = Square(int(move[2]), int(move[3]))
    return Move(src, dst)
