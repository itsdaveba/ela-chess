import re

from defs import Move, Square


def parse_move(move: str) -> Move | None:
    if re.fullmatch("[0-7]{4}", move) is None:
        return
    source = Square(int(move[0]), int(move[1]))
    target = Square(int(move[2]), int(move[3]))
    return Move(source, target)
