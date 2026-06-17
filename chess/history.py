from .move import Move
from .piece import Piece
from .square import Square


class History:
    def __init__(self) -> None:
        self.move_history: list[Move]
        self.capture_history: list[Piece | None]
        self.position_data_history: list[tuple[int, Square | None, int, list[Move]]]
        self.clear()

    def __repr__(self) -> str:
        return f"History({self.move_history!s})"

    def clear(self):
        self.move_history = []
        self.capture_history = []
        self.position_data_history = []

    def append(self, move: Move, capture: Piece | None, castling_rights: int,
               epsquare: Square | None, halfmove: int, pseudo_legal_moves: list[Move]):
        self.move_history.append(move)
        self.capture_history.append(capture)
        self.position_data_history.append((castling_rights, epsquare, halfmove, pseudo_legal_moves))

    def pop(self) -> tuple[Move, Piece | None, int, Square | None, int, list[Move]]:
        return (self.move_history.pop(), self.capture_history.pop()) + self.position_data_history.pop()

    def __len__(self):
        return len(self.move_history)
