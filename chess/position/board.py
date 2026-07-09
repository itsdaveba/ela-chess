from .color import Color
from .piece import Piece
from .castling import Castling
from .square import Square, Rank

from ..move.move import Move


EMPTY_BOARD_STRING: str = "8/8/8/8/8/8/8/8"
LAST_RANK: list[Rank] = [Rank.R8, Rank.R1]
SECOND_RANK: list[Rank] = [Rank.R2, Rank.R7]
DIRECTIONS: list[list[int]] = [
    [-10, 10],  # pawn
    [-21, -19, -12, -8, 8, 12, 19, 21],  # knight
    [-11, -9, 9, 11],  # bishop
    [-10, -1, 1, 10],  # rook
    [-11, -10, -9, -1, 1, 9, 10, 11],  # queen
    [-11, -10, -9, -1, 1, 9, 10, 11]  # king
]
castling_flags: list[Castling] = [Castling.WHITE_KINGSIDE | Castling.WHITE_QUEENSIDE,
                                  Castling.BLACK_KINGSIDE | Castling.BLACK_QUEENSIDE]
castling_info: list[tuple[list[Castling], list[list[Square]], list[list[Square]], list[Square]]] = [
    ([Castling.WHITE_KINGSIDE, Castling.WHITE_QUEENSIDE],
     [[Square.F1, Square.G1], [Square.D1, Square.C1, Square.B1]],
     [[Square.F1, Square.G1], [Square.D1, Square.C1]],
     [Square.G1, Square.C1]),
    ([Castling.BLACK_KINGSIDE, Castling.BLACK_QUEENSIDE],
     [[Square.F8, Square.G8], [Square.D8, Square.C8, Square.B8]],
     [[Square.F8, Square.G8], [Square.D8, Square.C8]],
     [Square.G8, Square.C8])
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
            if self.piece[move.source] != Piece.PAWN and move.target == square:
                return True

        single = square + DIRECTIONS[Piece.PAWN][side.opponent]
        for target in (single - 1, single + 1):
            if self.piece[target] == Piece.OFF:
                continue
            if self.color[target] == side and self.piece[target] == Piece.PAWN:
                return True

        return False

    def generate_pseudo_legal_moves(self, side: Color, castling: Castling, epsquare: Square) -> list[Move]:
        moves = []

        for source in Square:
            if self.color[source] != side:
                continue
            if self.piece[source] == Piece.PAWN:
                moves.extend(self._pawn_moves(side, source, epsquare))
            else:
                moves.extend(self._piece_moves(side, source))
                if self.piece[source] == Piece.KING and castling & castling_flags[side]:
                    if not self.is_attacked(source, side.opponent):
                        moves.extend(self._castle_moves(side, source, castling))

        return moves

    def _pawn_moves(self, side: Color, source: Square, epsquare: Square) -> list[Move]:
        moves = []

        single = Square(source + DIRECTIONS[Piece.PAWN][side])
        moves.extend(self._pawn_forward_moves(side, source, single))
        moves.extend(self._pawn_capture_moves(side, source, single, epsquare))

        return moves

    def _pawn_forward_moves(self, side: Color, source: Square, single: Square) -> list[Move]:
        moves = []

        if self.piece[single] == Piece.NONE:  # pawn forward
            moves.extend(self._pawn_promotion_moves(side, source, single))
            if source.rank == SECOND_RANK[side]:  # pawn double forward
                double = Square(single + DIRECTIONS[Piece.PAWN][side])
                if self.piece[double] == Piece.NONE:
                    moves.append(Move(source, double, Piece.NONE))

        return moves

    def _pawn_capture_moves(self, side: Color, source: Square, single: Square, epsquare: Square) -> list[Move]:
        moves = []

        for target in (single - 1, single + 1):
            if self.piece[target] == Piece.OFF:
                continue
            target = Square(target)
            if self.color[target] == Color.NONE:
                if target == epsquare:  # ep capture
                    moves.append(Move(source, target, Piece.NONE))
            elif self.color[target] != side:  # pawn capture
                moves.extend(self._pawn_promotion_moves(side, source, target))

        return moves

    def _pawn_promotion_moves(self, side: Color, source: Square, target: Square) -> list[Move]:
        if target.rank == LAST_RANK[side]:
            return [Move(source, target, prom) for prom in (Piece.KNIGHT, Piece.BISHOP, Piece.ROOK, Piece.QUEEN)]
        return [Move(source, target, Piece.NONE)]

    def _piece_moves(self, side: Color, source: Square) -> list[Move]:
        moves = []

        is_sliding = self.piece[source].is_sliding
        for direction in DIRECTIONS[self.piece[source]]:
            target = source
            while True:
                target += direction
                if self.piece[target] == Piece.OFF:
                    break
                target = Square(target)
                if self.color[target] != Color.NONE:
                    if self.color[target] != side:
                        moves.append(Move(source, target, Piece.NONE))
                    break
                moves.append(Move(source, target, Piece.NONE))
                if not is_sliding:
                    break

        return moves

    def _castle_moves(self, side: Color, source: Square, castling: Castling) -> list[Move]:
        moves = []

        for flag, empty_squares, not_attacked_squares, target in zip(*castling_info[side]):
            if castling & flag and self._can_castle(side, empty_squares, not_attacked_squares):
                moves.append(Move(source, target, Piece.NONE))

        return moves

    def _can_castle(self, side: Color, empty_squares: list[Square], not_attacked_squares: list[Square]) -> bool:
        for square in empty_squares:
            if self.piece[square] != Piece.NONE:
                return False
        for square in not_attacked_squares:
            if self.is_attacked(square, side.opponent):
                return False
        return True
