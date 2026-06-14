from .square import Square
from .history import History
from .castling import Castling
from .piece import Piece, ROOK, KING
from .board import Board, pawn_directions
from .move import Move, PAWN_MOVE, PAWN_DOUBLE_MOVE, CAPTURE


INITIAL_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

castling_rook_info = [("kq", ["h8", "a8"]), ("KQ", ["h1", "a1"])]


class Position:
    def __init__(self, fen: str = INITIAL_FEN) -> None:
        self.board: Board
        self.white: bool
        self.castling: Castling
        self.epsquare: Square | None
        self.halfmove: int
        self.fullmove: int
        self.history: History
        self._move_list: list[Move]

        self.fen = fen

    def __repr__(self) -> str:
        return f"Position('{self.fen}')"

    @property
    def move_list(self) -> list[Move]:
        if not self._move_list:
            self._move_list = self.board.generate_moves(self.white, self.castling, self.epsquare)
        return self._move_list

    @property
    def fen(self) -> str:
        fen_elements = [self.board.string]
        fen_elements.append("bw"[self.white])
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

        if len(fen_elements[1]) != 1 or fen_elements[1] not in "bw":
            raise ValueError(f"invalid fen color: {fen_elements[1]}")
        self.white = bool("bw".index(fen_elements[1]))

        self.castling = Castling(fen_elements[2])
        self.epsquare = None if fen_elements[3] == "-" else Square(fen_elements[3])

        if not fen_elements[4].isdigit():
            raise ValueError(f"invalid fen halfmove: {fen_elements[4]}")
        self.halfmove = int(fen_elements[4])

        if not fen_elements[5].isdigit() or int(fen_elements[5]) < 1:
            raise ValueError(f"invalid fen fullmove: {fen_elements[5]}")
        self.fullmove = int(fen_elements[5])

        self.history = History()
        self._move_list = []

    def reset(self) -> None:
        self.fen = INITIAL_FEN

    def _update_castling(self, piece: Piece, capture: Piece | None, move: Move) -> None:
        if piece.type == KING:
            self.castling.clear(castling_rook_info[piece.white][0])

        elif piece.type == ROOK:
            for flag, sqr_str in zip(*castling_rook_info[piece.white]):
                if self.castling & flag and move.source == sqr_str:
                    self.castling.clear(flag)

        if capture is not None and capture.type == ROOK:
            for flag, sqr_str in zip(*castling_rook_info[capture.white]):
                if self.castling & flag and move.target == sqr_str:
                    self.castling.clear(flag)

    def make_move(self, move: Move | str) -> bool:
        if isinstance(move, str):
            move = Move(move)

        if move not in self.move_list:
            return False

        move = self.move_list[self.move_list.index(move)]
        capture = self.board.make_move(self.white, move)

        if self.board.in_check(self.white):
            self.board.undo_move(self.white, move, capture)
            return False

        self.history.append(move, capture, self.castling.rights, self.epsquare, self.halfmove)

        piece = self.board[move.target]
        assert piece is not None
        self._update_castling(piece, capture, move)

        self.epsquare = move.target + pawn_directions[not self.white] if move.type & PAWN_DOUBLE_MOVE else None
        self.halfmove = 0 if move.type & (PAWN_MOVE | CAPTURE) else self.halfmove + 1
        if not self.white:
            self.fullmove += 1
        self.white = not self.white
        self._move_list = []

        return True

    def undo_move(self) -> None:
        if not self.history:
            raise ValueError("no previous moves")

        move, capture, self.castling.rights, self.epsquare, self.halfmove = self.history.pop()
        self.white = not self.white

        self.board.undo_move(self.white, move, capture)
        if not self.white:
            self.fullmove -= 1
        self._move_list = []
