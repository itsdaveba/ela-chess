from .color import Color
from .piece import Piece
from .square import Square
from .counter import Counter
from .castling import Castling
from .board import Board, DIRECTIONS, CASTLING_FLAGS

from ..move.move import Move, MoveType


CASTLING_ROOK_INFO: list[dict[Castling, Square]] = [
    {Castling.WHITE_KINGSIDE: Square.H1, Castling.WHITE_QUEENSIDE: Square.A1},
    {Castling.BLACK_KINGSIDE: Square.H8, Castling.BLACK_QUEENSIDE: Square.A8}
]


class Position:
    def __init__(self, fen: str) -> None:
        self.board: Board
        self.side: Color
        self.castling: Castling
        self.epsquare: Square
        self.halfmove: Counter
        self.fullmove: Counter

        self.fen = fen

    def __repr__(self) -> str:
        return f"Position('{self.fen}')"

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
    def pseudo_legal_moves(self) -> list[Move]:
        return self.board.generate_pseudo_legal_moves(self.side, self.castling, self.epsquare)

    def in_check(self, side: Color) -> bool:
        return self.board.in_check(side)

    def make_move(self, move: Move) -> tuple[Piece, Castling, Square, Counter]:
        capture = self.board.make_move(self.side, move)

        irrev = capture, self.castling, self.epsquare, self.halfmove.copy()

        if self.castling:
            if move.piece == Piece.KING:
                self.castling &= ~CASTLING_FLAGS[self.side]
            elif move.piece == Piece.ROOK:
                for flag, square in CASTLING_ROOK_INFO[self.side].items():
                    if move.origin == square:
                        self.castling &= ~flag
            if capture == Piece.ROOK:
                for flag, square in CASTLING_ROOK_INFO[self.side.opponent].items():
                    if move.target == square:
                        self.castling &= ~flag

        if move.type & MoveType.PAWN_DOUBLE_MOVE:
            self.epsquare = Square(move.origin + DIRECTIONS[Piece.PAWN][self.side])
        else:
            self.epsquare = Square.NONE

        if move.type & (MoveType.PAWN_MOVE | MoveType.CAPTURE):
            self.halfmove.reset()
        else:
            self.halfmove.incr()

        if self.side == Color.BLACK:
            self.fullmove.incr()

        self.side = self.side.opponent

        return irrev

    def undo_move(self, move: Move, irrev: tuple[Piece, Castling, Square, Counter]) -> None:
        self.side = self.side.opponent

        capture, self.castling, self.epsquare, self.halfmove = irrev

        self.board.undo_move(self.side, move, capture)

        if self.side == Color.BLACK:
            self.fullmove.decr()
