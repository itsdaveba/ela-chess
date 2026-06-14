from .color import Color
from .castling import Castling
from .square import File, Rank, Square
from .move import Move, PAWN_MOVE, PAWN_DOUBLE_MOVE, PROMOTION, CAPTURE, EP_CAPTURE, CASTLE
from .piece import PieceType, Piece, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING


NORTH_EAST = (1, -1)
NORTH_WEST = (-1, -1)
SOUTH_EAST = (1, 1)
SOUTH_WEST = (-1, 1)

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)

NORTH_EAST_NORTH = (1, -2)
NORTH_EAST_EAST = (2, -1)
NORTH_WEST_NORTH = (-1, -2)
NORTH_WEST_WEST = (-2, -1)

SOUTH_EAST_SOUTH = (1, 2)
SOUTH_EAST_EAST = (2, 1)
SOUTH_WEST_SOUTH = (-1, 2)
SOUTH_WEST_WEST = (-2, 1)


pawn_directions = [SOUTH, NORTH]
piece_directions: dict[int, list[tuple[int, int]]] = {
    KNIGHT: [NORTH_EAST_NORTH, NORTH_EAST_EAST, NORTH_WEST_NORTH, NORTH_WEST_WEST,
             SOUTH_EAST_SOUTH, SOUTH_EAST_EAST, SOUTH_WEST_SOUTH, SOUTH_WEST_WEST],
    BISHOP: [NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST],
    ROOK: [NORTH, SOUTH, EAST, WEST],
    QUEEN: [NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST, NORTH, SOUTH, EAST, WEST],
    KING: [NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST, NORTH, SOUTH, EAST, WEST],
}

castling_squares = {"g1": ("f1", "h1"), "c1": ("d1", "a1"), "g8": ("f8", "h8"), "c8": ("d8", "a8")}
castling_king_info = [
    ("kq", (["f8", "g8"], ["d8", "c8", "b8"]), (["e8", "f8", "g8"], ["e8", "d8", "c8"]), ["g8", "c8"]),
    ("KQ", (["f1", "g1"], ["d1", "c1", "b1"]), (["e1", "f1", "g1"], ["e1", "d1", "c1"]), ["g1", "c1"])
]


class Board:
    def __init__(self) -> None:
        self.grid: dict[Square, Piece | None]
        self.clear()

    def __repr__(self) -> str:
        return f"Board('{self.string}')"

    def __getitem__(self, key: Square) -> Piece | None:
        return self.grid[key]

    @property
    def string(self) -> str:
        piece_placement = []

        for rank in Rank:
            row, count = "", 0

            for file in File:
                piece = self.grid[Square(file, rank)]
                if piece is not None:
                    if count:
                        row += str(count)
                        count = 0
                    row += piece.char
                    continue
                count += 1
            if count:
                row += str(count)

            piece_placement.append(row)

        return "/".join(piece_placement)

    @string.setter
    def string(self, string: str) -> None:
        ranks: list[str] = string.split("/")
        if len(ranks) != 8:
            raise ValueError(f"invalid board string; {string}")

        grid: list[list[Piece | None]] = []
        for rank in ranks:
            grid.append([])
            for char in rank:
                if char.isdigit():
                    grid[-1].extend([None] * int(char))
                else:
                    grid[-1].append(Piece(char))

            if len(grid[-1]) != 8:
                raise ValueError(f"invalid board string: {string}")

        self.grid = {square: grid[square.rank.value][square.file.value] for square in Square}

    def clear(self):
        self.grid = {square: None for square in Square}

    def is_attacked(self, side: Color, square: Square) -> bool:
        for move in self.generate_moves(side):
            if not move.type & PAWN_MOVE and move.target == square:
                return True
        try:
            single = square + pawn_directions[not side.white]
        except ValueError:
            return False
        for dir in (EAST, WEST):
            try:
                target = single + dir
            except ValueError:
                continue
            piece = self.grid[target]
            if piece is not None and piece.color == side and piece.type == PAWN:
                return True
        return False

    def in_check(self, side: Color) -> bool:
        for square in Square:
            piece = self.grid[square]
            if piece is not None and piece.type == KING and piece.color == side:
                return self.is_attacked(side.opponent, square)
        return False

    def make_move(self, side: Color, move: Move) -> Piece | None:
        capture = self.grid[move.target]

        self.grid[move.target] = Piece(side, move.promotion) if move.type & PROMOTION else self.grid[move.source]
        self.grid[move.source] = None

        if move.type & EP_CAPTURE:
            self.grid[move.target + pawn_directions[not side.white]] = None

        elif move.type & CASTLE:
            free_sqr, rook_sqr = castling_squares[move.target.string]
            self.grid[Square(free_sqr)] = self.grid[Square(rook_sqr)]
            self.grid[Square(rook_sqr)] = None

        return capture

    def undo_move(self, side: Color, move: Move, capture: Piece | None) -> None:
        self.grid[move.source] = Piece(side, PieceType(PAWN)) if move.type & PROMOTION else self.grid[move.target]
        self.grid[move.target] = capture

        if move.type & EP_CAPTURE:
            self.grid[move.target + pawn_directions[not side.white]] = Piece(side.opponent, PieceType(PAWN))

        elif move.type & CASTLE:
            free_sqr, rook_sqr = castling_squares[move.target.string]
            self.grid[Square(rook_sqr)] = self.grid[Square(free_sqr)]
            self.grid[Square(free_sqr)] = None

    def _pawn_promotion_moves(self, side: Color, source: Square, target: Square, is_capture: bool) -> list[Move]:
        flags = (PAWN_MOVE | CAPTURE) if is_capture else PAWN_MOVE

        if target.rank == (Rank('8') if side.white else Rank('1')):
            flags |= PROMOTION
            return [Move(source, target, flags, prom) for prom in (KNIGHT, BISHOP, ROOK, QUEEN)]

        return [Move(source, target, flags, None)]

    def _pawn_forward_moves(self, side: Color, source: Square, single: Square, direction: tuple[int, int]) -> list[Move]:
        moves: list[Move] = []

        if self.grid[single] is None:
            moves.extend(self._pawn_promotion_moves(side, source, single, False))
            if source.rank == (Rank('2') if side.white else Rank('7')):
                double = single + direction
                if self.grid[double] is None:
                    moves.append(Move(source, double, PAWN_MOVE | PAWN_DOUBLE_MOVE, None))

        return moves

    def _pawn_capture_moves(self, side: Color, source: Square, single: Square, epsquare: Square | None) -> list[Move]:
        moves: list[Move] = []

        for dir in (EAST, WEST):
            try:
                target = single + dir
            except ValueError:
                continue
            capture = self.grid[target]
            if capture is not None and capture.color != side:
                moves.extend(self._pawn_promotion_moves(side, source, target, True))
            elif target == epsquare:
                moves.append(Move(source, target, PAWN_MOVE | CAPTURE | EP_CAPTURE, None))

        return moves

    def _pawn_moves(self, side: Color, source: Square, epsquare: Square | None) -> list[Move]:
        moves: list[Move] = []

        direction = pawn_directions[side.white]
        single = source + direction

        moves.extend(self._pawn_forward_moves(side, source, single, direction))
        moves.extend(self._pawn_capture_moves(side, source, single, epsquare))

        return moves

    def _piece_moves(self, side: Color, source: Square, piece: Piece) -> list[Move]:
        moves: list[Move] = []

        for direction in piece_directions[piece.type.value]:
            target = source
            while True:
                try:
                    target += direction
                except ValueError:
                    break
                capture = self.grid[target]
                if capture is not None:
                    if capture.color != side:
                        moves.append(Move(source, target, CAPTURE, None))
                    break
                moves.append(Move(source, target, 0, None))
                if not piece.type.sliding:
                    break

        return moves

    def _can_castle(self, side: Color, empty_sqrs: list[str], no_attacked_sqrs: list[str]) -> bool:
        for sqr in empty_sqrs:
            if self.grid[Square(sqr)] is not None:
                return False
        for sqr in no_attacked_sqrs:
            if self.is_attacked(side.opponent, Square(sqr)):
                return False
        return True

    def _castle_moves(self, side: Color, source: Square, castling: Castling) -> list[Move]:
        moves: list[Move] = []

        for flag, empty_sqrs, no_attacked_sqrs, target_sqr in zip(*castling_king_info[side.white]):
            if castling & flag and self._can_castle(side, empty_sqrs, no_attacked_sqrs):
                moves.append(Move(source, Square(target_sqr), CASTLE, None))

        return moves

    def generate_moves(self, side: Color, castling: Castling = Castling(0), epsquare: Square | None = None) -> list[Move]:
        moves: list[Move] = []

        for source in Square:
            piece = self.grid[source]
            if piece is None or piece.color != side:
                continue
            if piece.type == PAWN:
                moves.extend(self._pawn_moves(side, source, epsquare))
                continue
            moves.extend(self._piece_moves(side, source, piece))
            if piece.type == KING:
                moves.extend(self._castle_moves(side, source, castling))

        return moves
