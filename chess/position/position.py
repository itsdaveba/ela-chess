import random

from .color import Color
from .piece import Piece
from .square import Square
from .counter import Counter
from .castling import Castling
from .board import Board, PAWN_FORWARD, CASTLING_FLAGS, ATTACK_SQUARES

from ..move.move import Move, MoveType


SIDE_STRING: list[str] = ["White", "Black"]
CASTLING_ROOK_INFO: list[list[tuple[Castling, Square]]] = [
    [(Castling.WHITE_KINGSIDE, Square.H1), (Castling.WHITE_QUEENSIDE, Square.A1)],
    [(Castling.BLACK_KINGSIDE, Square.H8), (Castling.BLACK_QUEENSIDE, Square.A8)]
]
HASH_SIDE: list[int] = [0, random.getrandbits(64)]
HASH_CASTLING_FLAGS: list[int] = [random.getrandbits(64) for _ in range(4)]
HASH_CASTLING: list[int] = [0] * 16
for castling in range(16):
    hash = 0
    for i, flag in enumerate(Castling):
        if castling & flag:
            hash ^= HASH_CASTLING_FLAGS[i]
    HASH_CASTLING[castling] = hash
HASH_EPSQUARE: list[int] = [random.getrandbits(64) for _ in range(8)] + [0]


def perft(position: "Position", depth: int) -> int:
    if depth == 0:
        return 1

    nodes = 0
    side = position.side

    for move in position.pseudo_legal_moves:
        irrev = position.make_move(move)
        if not position.in_check(side):
            nodes += perft(position, depth - 1)
        position.undo_move(move, irrev)

    return nodes


class Position:
    def __init__(self, fen: str) -> None:
        self.board: Board
        self.side: Color
        self.castling: Castling
        self.epsquare: Square
        self.halfmove: Counter
        self.fullmove: Counter
        self.hash: int

        self.fen = fen

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Position):
            return self.hash == other.hash
        return False

    def __repr__(self) -> str:
        return f"Position('{self.fen}')"

    def __str__(self) -> str:
        rows = [f"{SIDE_STRING[self.side]} to move"]

        rows.append("+-----------------+")

        for i, row in enumerate(str(self.board).split("\n")):
            rows.append(f"| {row} | {8 - i}")

        rows.append("+-----------------+")
        rows.append("  a b c d e f g h")

        return "\n".join(rows)

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

        self.hash = self.board.hash
        self.hash ^= HASH_SIDE[self.side]
        self.hash ^= HASH_CASTLING[self.castling]
        self.hash ^= HASH_EPSQUARE[self.epsquare.file]
        self._update_epsquare(self.side)

    @property
    def eval(self) -> int:
        return self.board.eval

    @property
    def pseudo_legal_moves(self) -> list[Move]:
        return self.board.generate_pseudo_legal_moves(self.side, self.castling, self.epsquare)

    def copy(self) -> "Position":
        return Position(self.fen)

    def in_check(self, side: Color) -> bool:
        return self.board.in_check(side)

    def make_move(self, move: Move) -> tuple[Piece, Castling, Square, Counter, int]:
        hash = self.hash

        self.hash ^= self.board.hash
        capture = self.board.make_move(self.side, move)
        self.hash ^= self.board.hash

        irrev = capture, self.castling, self.epsquare, self.halfmove.copy(), hash

        if self.castling:
            if self.board.piece[move.target] == Piece.KING:
                if self.castling & CASTLING_FLAGS[self.side]:
                    self.hash ^= HASH_CASTLING[self.castling]
                    self.castling &= ~CASTLING_FLAGS[self.side]
                    self.hash ^= HASH_CASTLING[self.castling]
            elif self.board.piece[move.target] == Piece.ROOK:
                for flag, square in CASTLING_ROOK_INFO[self.side]:
                    if move.origin == square and self.castling & flag:
                        self.castling &= ~flag
                        self.hash ^= HASH_CASTLING[flag]
            if capture == Piece.ROOK:
                for flag, square in CASTLING_ROOK_INFO[self.side.opponent]:
                    if move.target == square and self.castling & flag:
                        self.castling &= ~flag
                        self.hash ^= HASH_CASTLING[flag]

        if move.type & MoveType.PAWN_DOUBLE_MOVE:
            if self.epsquare != Square.NONE:
                self.hash ^= HASH_EPSQUARE[self.epsquare.file]
            self.epsquare = PAWN_FORWARD[self.side][move.origin]
            self.hash ^= HASH_EPSQUARE[self.epsquare.file]
            self._update_epsquare(self.side.opponent)
        elif self.epsquare != Square.NONE:
            self.hash ^= HASH_EPSQUARE[self.epsquare.file]
            self.epsquare = Square.NONE

        if move.type & (MoveType.PAWN_MOVE | MoveType.CAPTURE):
            self.halfmove.reset()
        else:
            self.halfmove.incr()

        if self.side == Color.BLACK:
            self.fullmove.incr()

        self.side = self.side.opponent
        self.hash ^= HASH_SIDE[Color.BLACK]

        return irrev

    def undo_move(self, move: Move, irrev: tuple[Piece, Castling, Square, Counter, int]) -> None:
        self.side = self.side.opponent

        capture, self.castling, self.epsquare, self.halfmove, self.hash = irrev

        self.board.undo_move(self.side, move, capture)

        if self.side == Color.BLACK:
            self.fullmove.decr()

    def _update_epsquare(self, side: Color) -> None:
        if self.epsquare != Square.NONE:
            legal_epcapture = False
            type = MoveType.PAWN_MOVE | MoveType.EPCAPTURE | MoveType.CAPTURE

            for origin in ATTACK_SQUARES[Piece.PAWN][side.opponent][self.epsquare]:
                if self.board.piece[origin] == Piece.PAWN and self.board.color[origin] == side:
                    epmove = Move(origin, self.epsquare, type)
                    capture = self.board.make_move(side, epmove)
                    if not self.board.in_check(side):
                        legal_epcapture = True
                    self.board.undo_move(side, epmove, capture)

            if not legal_epcapture:
                self.hash ^= HASH_EPSQUARE[self.epsquare.file]
                self.epsquare = Square.NONE
