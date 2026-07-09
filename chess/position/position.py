from .color import Color
from .board import Board
from .square import Square
from .counter import Counter
from .castling import Castling


STARTING_POSITION_FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


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
