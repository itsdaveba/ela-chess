from ..position.piece import Piece
from ..position.square import Square
from ..position.counter import Counter
from ..position.castling import Castling

from ..move.move import Move


class History:
    def __init__(self) -> None:
        self.moves: list[Move]
        self.captures: list[Piece]
        self.irrevs: list[tuple[Castling, Square, Counter]]  # TODO check all tuple types

    def append(self, move: Move, capture: Piece, irrev: tuple[Castling, Square, Counter]) -> None:
        self.moves.append(move)
        self.captures.append(capture)
        self.irrevs.append(irrev)

    def pop(self) -> tuple[Move, Piece, tuple[Castling, Square, Counter]]:
        return self.moves.pop(), self.captures.pop(), self.irrevs.pop()
