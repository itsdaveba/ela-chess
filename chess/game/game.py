from .history import History

from ..position.position import Position


class ChessGame:
    def __init__(self) -> None:
        self.position: Position
        self.history: History
