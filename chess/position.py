from .board import Board, pawn_direction
from .color import Color
from .castling import Castling
from .square import Square
from .move import Move, PAWN_DOUBLE_MOVE, PAWN_MOVE, CAPTURE
from .piece import Piece, KING, ROOK


INITIAL_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class Position:
    def __init__(self, fen: str = INITIAL_FEN) -> None:
        self.board: Board
        self.side: Color
        self.castling: Castling
        self.epsquare: Square | None
        self.halfmove: int
        self.fullmove: int
        self.history: list[tuple[Move, Piece | None, int, Square | None, int]] = []

        self._move_list: list[Move] = []

        self.fen = fen

    def __repr__(self) -> str:
        return f"Position('{self.fen}')"

    @property
    def move_list(self) -> list[Move]:
        if not self._move_list:
            self._move_list = self.board.generate_moves(self.side, self.castling, self.epsquare)
        return self._move_list

    @property
    def fen(self) -> str:
        fen_elements = [self.board.string]
        fen_elements.append(self.side.char)
        fen_elements.append(self.castling.string)
        fen_elements.append("-" if self.epsquare is None else self.epsquare.string)
        fen_elements.append(str(self.halfmove))
        fen_elements.append(str(self.fullmove))
        return " ".join(fen_elements)

    @fen.setter
    def fen(self, fen: str) -> None:
        fen_elements = fen.split()

        if len(fen_elements) != 6:
            raise ValueError(f"invalid fen: {fen}")

        self.board = Board()
        self.board.string = fen_elements[0]
        self.side = Color(fen_elements[1])
        self.castling = Castling(fen_elements[2])
        self.epsquare = None if fen_elements[3] == "-" else Square(fen_elements[3])
        self.halfmove = int(fen_elements[4])  # TODO maybe remove Counter
        self.fullmove = int(fen_elements[5])

    def reset(self) -> None:
        self.fen = INITIAL_FEN

    def _update_castling(self, piece: Piece, capture: Piece | None, move: Move) -> None:
        if piece.type == KING:
            self.castling.clear(castling_info[piece.color.white][0])

        elif piece.type == ROOK:
            for flag, sqr_str in zip(*castling_info[piece.color.white]):
                if self.castling & flag and move.source == sqr_str:
                    self.castling.clear(flag)

        if capture is not None and capture.type == ROOK:
            for flag, sqr_str in zip(*castling_info[capture.color.white]):
                if self.castling & flag and move.target == sqr_str:
                    self.castling.clear(flag)

    def make_move(self, move: Move | str) -> bool:
        if isinstance(move, str):
            move = Move(move)

        if move not in self.move_list:
            print("illegal move")
            return False

        move = self.move_list[self.move_list.index(move)]
        capture = self.board.make_move(self.side, move)

        if self.board.in_check(self.side):
            self.board.undo_move(self.side, move, capture)
            return False

        self.history.append((move, capture, self.castling.rights, self.epsquare, self.halfmove))

        piece = self.board[move.target]
        assert piece is not None
        self._update_castling(piece, capture, move)

        self.epsquare = move.target + pawn_direction[not self.side.white] if move.type & PAWN_DOUBLE_MOVE else None
        self.halfmove = 0 if move.type & (PAWN_MOVE | CAPTURE) else self.halfmove + 1
        if not self.side.white:
            self.fullmove += 1
        self.side = self.side.opponent
        self._move_list = []

        return True

    def undo_move(self) -> None:
        if not self.history:
            raise ValueError("no previous moves")

        move, capture, self.castling.rights, self.epsquare, self.halfmove = self.history.pop()

        self.board.undo_move(self.side, move, capture)
        if self.side.white:
            self.fullmove -= 1
        self.side = self.side.opponent
        self._move_list = []


castling_info = [
    ("kq", ["h8", "a8"]),
    ("KQ", ["h1", "a1"])
]
