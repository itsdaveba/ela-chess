from .color import Color
from .piece import Piece
from .square import Square
from .counter import Counter
from .castling import Castling
from .board import Board, CASTLING_FLAGS

from ..move.move import Move, MoveType


STARTING_POSITION_FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
CASTLING_ROOK_INFO: list[dict[Castling, Square]] = [
    {Castling.WHITE_KINGSIDE: Square.H1, Castling.WHITE_QUEENSIDE: Square.A1},
    {Castling.BLACK_KINGSIDE: Square.H8, Castling.BLACK_QUEENSIDE: Square.A8}
]


class Position:
    def __init__(self, fen: str = STARTING_POSITION_FEN) -> None:
        self.board: Board
        self.side: Color
        self.castling: Castling
        self.epsquare: Square
        self.halfmove: Counter
        self.fullmove: Counter

        self.fen = fen

    @property
    def fen(self) -> str:
        fen_elements = []

        fen_elements.append(self.board.string)
        fen_elements.append(self.side.char)
        fen_elements.append(self.castling.string)
        fen_elements.append(self.epsquare.string)
        fen_elements.append(self.halfmove.string)
        fen_elements.append(self.fullmove.string)

        return " ".join(fen_elements)

    @fen.setter
    def fen(self, fen: str) -> None:
        fen_elements = fen.split()
        if len(fen_elements) != 6:
            raise ValueError(f"invalid fen: '{fen}'")

        self.board = Board(fen_elements[0])
        self.side = Color.from_char(fen_elements[1])
        self.castling = Castling.from_string(fen_elements[2])
        self.epsquare = Square.from_string(fen_elements[3])
        self.halfmove = Counter.from_string(fen_elements[4])
        self.fullmove = Counter.from_string(fen_elements[5])

    @property
    def pseudo_legal_moves(self) -> list[Move]:  # TODO cached
        return self.board.generate_pseudo_legal_moves(self.side, self.castling, self.epsquare)

    def make_move(self, move: Move) -> None:
        capture = self.board.make_move(move)
        self.history.append(move, capture, (self.castling, self.epsquare, self.halfmove))
        self.side = self.side.opponent

    def undo_move(self) -> None:
        move, capture, irrev = self.history.pop()
        self.board.undo_move(move, capture)
