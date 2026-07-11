from .history import History

from ..move.move import Move

from ..position.position import Position


STARTING_POSITION_FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class ChessGame:
    def __init__(self, fen: str = STARTING_POSITION_FEN) -> None:
        self.fen: str = fen
        self.position: Position = Position(fen)
        self.history: History = History()

    def __repr__(self) -> str:
        if self.fen == STARTING_POSITION_FEN:
            return f"ChessGame(history={self.history.moves})"
        return f"ChessGame(fen='{self.fen}', history={self.history.moves})"

    def make_move(self, move: Move) -> bool:

        side = self.position.side
        moves = self.position.pseudo_legal_moves

        try:
            move = moves[moves.index(move)]
        except ValueError:
            return False

        irrev = self.position.make_move(move)

        if self.position.in_check(side):
            self.position.undo_move(move, irrev)
            return False

        self.history.append(move, irrev)

        return True

    def undo_move(self) -> None:
        try:
            move, irrev = self.history.pop()
        except IndexError:
            raise ValueError("no previous move")

        self.position.undo_move(move, irrev)
