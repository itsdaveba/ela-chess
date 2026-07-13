from .color import Color
from .piece import Piece
from .castling import Castling
from .square import Square, Rank

from ..move.move import Move, MoveType

EMPTY_BOARD_STRING: str = "8/8/8/8/8/8/8/8"
SECOND_RANK: list[Rank] = [Rank.R2, Rank.R7]
DIRECTIONS: list[list[int]] = [
    [-10, 10],  # pawn
    [-21, -19, -12, -8, 8, 12, 19, 21],  # knight
    [-11, -9, 9, 11],  # bishop
    [-10, -1, 1, 10],  # rook
    [-11, -10, -9, -1, 1, 9, 10, 11],  # queen
    [-11, -10, -9, -1, 1, 9, 10, 11]  # king
]
CASTLING_FLAGS: list[Castling] = [
    Castling.WHITE_KINGSIDE | Castling.WHITE_QUEENSIDE,
    Castling.BLACK_KINGSIDE | Castling.BLACK_QUEENSIDE
]
CASTLING_INFO: list[tuple[list[Castling], list[list[Square]], list[list[Square]], list[Square]]] = [
    ([Castling.WHITE_KINGSIDE, Castling.WHITE_QUEENSIDE],
     [[Square.F1, Square.G1], [Square.D1, Square.C1, Square.B1]],
     [[Square.F1, Square.G1], [Square.D1, Square.C1]],
     [Square.G1, Square.C1]),
    ([Castling.BLACK_KINGSIDE, Castling.BLACK_QUEENSIDE],
     [[Square.F8, Square.G8], [Square.D8, Square.C8, Square.B8]],
     [[Square.F8, Square.G8], [Square.D8, Square.C8]],
     [Square.G8, Square.C8])
]
CASTLING_KING_INFO: list[dict[Square, tuple[Square, Square]]] = [
    {Square.G1: (Square.H1, Square.F1), Square.C1: (Square.A1, Square.D1)},
    {Square.G8: (Square.H8, Square.F8), Square.C8: (Square.A8, Square.D8)}
]


class Board:
    def __init__(self, string: str = EMPTY_BOARD_STRING) -> None:
        self.color: list[Color]
        self.piece: list[Piece]

        self.string = string

    def __repr__(self) -> str:
        return self.string

    def __str__(self) -> str:
        ranks = []

        for r in range(8):
            rank = []
            color_rank = self.color[r * 10:]
            piece_rank = self.piece[r * 10:]
            for f in range(1, 9):
                rank.append(piece_rank[f].char.lower() if color_rank[f] == Color.BLACK else piece_rank[f].char)
            ranks.append(" ".join(rank))

        return "\n".join(ranks)

    @property
    def string(self) -> str:
        ranks = []

        for r in range(8):
            rank = ""
            count = 0
            color_rank = self.color[r * 10:]
            piece_rank = self.piece[r * 10:]
            for f in range(1, 9):
                piece = piece_rank[f]
                if piece == Piece.NONE:
                    count += 1
                    continue
                if count:
                    rank += str(count)
                    count = 0
                rank += piece.char.lower() if color_rank[f] == Color.BLACK else piece.char
            if count:
                rank += str(count)
            ranks.append(rank)

        return "/".join(ranks)

    @string.setter
    def string(self, string: str) -> None:
        self.color = []
        self.piece = []

        ranks = string.split("/")
        if len(ranks) != 8:
            raise ValueError(f"invalid board string: '{string}'")

        for rank in ranks:
            color_rank = [Color.NONE]
            piece_rank = [Piece.OFF]
            for char in rank:
                if char.isdigit():
                    color_rank.extend([Color.NONE] * int(char))
                    piece_rank.extend([Piece.NONE] * int(char))
                else:
                    color_rank.append(Color.WHITE if char.isupper() else Color.BLACK)
                    piece_rank.append(Piece.from_char(char.upper()))
            if len(piece_rank) != 9:
                raise ValueError(f"invalid board string: '{string}'")

            color_rank.append(Color.NONE)
            piece_rank.append(Piece.OFF)

            self.color.extend(color_rank)
            self.piece.extend(piece_rank)

        self.color.extend([Color.NONE] * 20)
        self.piece.extend([Piece.OFF] * 20)

    def is_attacked(self, square: Square, side: Color) -> bool:
        for move in self.generate_pseudo_legal_moves(side, Castling.NONE, Square.NONE):
            if self.piece[move.origin] != Piece.PAWN and move.target == square:
                return True

        single = square + DIRECTIONS[Piece.PAWN][side.opponent]
        for target in (single - 1, single + 1):
            if self.piece[target] == Piece.OFF:
                continue
            if self.color[target] == side and self.piece[target] == Piece.PAWN:
                return True

        return False

    def in_check(self, side: Color) -> bool:
        for square in Square:
            if self.piece[square] == Piece.KING and self.color[square] == side:
                return self.is_attacked(square, side.opponent)
        return False

    def generate_pseudo_legal_moves(self, side: Color, castling: Castling, epsquare: Square) -> list[Move]:
        moves = []

        for origin in Square:
            if self.color[origin] != side:
                continue
            if self.piece[origin] == Piece.PAWN:
                moves.extend(self._pawn_moves(side, origin, epsquare))
            else:
                moves.extend(self._piece_moves(side, origin))
                if self.piece[origin] == Piece.KING and castling & CASTLING_FLAGS[side]:
                    moves.extend(self._castle_moves(side, origin, castling))
        return moves

    def _pawn_moves(self, side: Color, origin: Square, epsquare: Square) -> list[Move]:
        moves = []

        single = Square(origin + DIRECTIONS[Piece.PAWN][side])
        moves.extend(self._pawn_forward_moves(side, origin, single))
        moves.extend(self._pawn_capture_moves(side, origin, single, epsquare))

        return moves

    def _pawn_forward_moves(self, side: Color, origin: Square, single: Square) -> list[Move]:
        moves = []

        type = MoveType.PAWN_MOVE
        if self.piece[single] == Piece.NONE:
            moves.extend(self._pawn_promotion_moves(side, origin, single, type))
            if origin.rank == SECOND_RANK[side]:
                double = Square(single + DIRECTIONS[Piece.PAWN][side])
                if self.piece[double] == Piece.NONE:
                    moves.append(Move(origin, double, type | MoveType.PAWN_DOUBLE_MOVE))

        return moves

    def _pawn_capture_moves(self, side: Color, origin: Square, single: Square, epsquare: Square) -> list[Move]:
        moves = []

        type = MoveType.PAWN_MOVE | MoveType.CAPTURE
        for target in (single - 1, single + 1):
            if self.piece[target] == Piece.OFF:
                continue
            target = Square(target)
            if self.color[target] == Color.NONE:
                if target == epsquare:
                    moves.append(Move(origin, target, type | MoveType.EPCAPTURE))
            elif self.color[target] != side:
                moves.extend(self._pawn_promotion_moves(side, origin, target, type))

        return moves

    def _pawn_promotion_moves(self, side: Color, origin: Square, target: Square, type: MoveType) -> list[Move]:
        if origin.rank == SECOND_RANK[side.opponent]:
            moves = []
            for promotion in (Piece.KNIGHT, Piece.BISHOP, Piece.ROOK, Piece.QUEEN):
                moves.append(Move(origin, target, type | MoveType.PROMOTION, promotion))
            return moves
        return [Move(origin, target, type)]

    def _piece_moves(self, side: Color, origin: Square) -> list[Move]:
        moves = []

        piece = self.piece[origin]
        is_sliding = piece.is_sliding
        for direction in DIRECTIONS[piece]:
            target = origin
            while True:
                target += direction
                if self.piece[target] == Piece.OFF:
                    break
                target = Square(target)
                if self.color[target] != Color.NONE:
                    if self.color[target] != side:
                        moves.append(Move(origin, target, MoveType.CAPTURE))
                    break
                moves.append(Move(origin, target, MoveType.NONE))
                if not is_sliding:
                    break

        return moves

    def _castle_moves(self, side: Color, origin: Square, castling: Castling) -> list[Move]:
        moves = []

        if not self.is_attacked(origin, side.opponent):
            for flag, empty_squares, not_attacked_squares, target in zip(*CASTLING_INFO[side]):
                if castling & flag and self._can_castle(side, empty_squares, not_attacked_squares):
                    moves.append(Move(origin, target, MoveType.CASTLE))

        return moves

    def _can_castle(self, side: Color, empty_squares: list[Square], not_attacked_squares: list[Square]) -> bool:
        for square in empty_squares:
            if self.piece[square] != Piece.NONE:
                return False
        for square in not_attacked_squares:
            if self.is_attacked(square, side.opponent):
                return False
        return True

    def make_move(self, side: Color, move: Move) -> Piece:
        capture = self.piece[move.target]

        self.color[move.target] = self.color[move.origin]
        self.piece[move.target] = move.promotion if move.type & MoveType.PROMOTION else self.piece[move.origin]

        self.color[move.origin] = Color.NONE
        self.piece[move.origin] = Piece.NONE

        if move.type & MoveType.EPCAPTURE:
            target = move.target + DIRECTIONS[Piece.PAWN][side.opponent]
            self.color[target] = Color.NONE
            self.piece[target] = Piece.NONE

        if move.type & MoveType.CASTLE:
            origin, target = CASTLING_KING_INFO[side][move.target]

            self.color[target] = self.color[origin]
            self.piece[target] = self.piece[origin]

            self.color[origin] = Color.NONE
            self.piece[origin] = Piece.NONE

        return capture

    def undo_move(self, side: Color, move: Move, capture: Piece) -> None:
        self.color[move.origin] = self.color[move.target]
        self.piece[move.origin] = Piece.PAWN if move.type & MoveType.PROMOTION else self.piece[move.target]

        is_normal_capture = move.type & (MoveType.CAPTURE | MoveType.EPCAPTURE) == MoveType.CAPTURE
        self.color[move.target] = side.opponent if is_normal_capture else Color.NONE
        self.piece[move.target] = capture

        if move.type & MoveType.EPCAPTURE:
            target = move.target + DIRECTIONS[Piece.PAWN][side.opponent]
            self.color[target] = side.opponent
            self.piece[target] = Piece.PAWN

        if move.type & MoveType.CASTLE:
            origin, target = CASTLING_KING_INFO[side][move.target]

            self.color[origin] = self.color[target]
            self.piece[origin] = self.piece[target]

            self.color[target] = Color.NONE
            self.piece[target] = Piece.NONE
