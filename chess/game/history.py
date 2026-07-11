from ..position.piece import Piece
from ..position.square import Square
from ..position.counter import Counter
from ..position.castling import Castling

from ..move.move import Move


class History:
    def __init__(self) -> None:
        self.moves: list[Move] = []
        self.irrevs: list[tuple[Piece, Castling, Square, Counter]] = []

    def __repr__(self) -> str:
        return f"History({self.moves})"

    def __len__(self) -> int:
        return len(self.moves)

    def append(self, move: Move, irrev: tuple[Piece, Castling, Square, Counter]) -> None:
        self.moves.append(move)
        self.irrevs.append(irrev)

    def pop(self) -> tuple[Move, tuple[Piece, Castling, Square, Counter]]:
        return self.moves.pop(), self.irrevs.pop()
