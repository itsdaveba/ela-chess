from .castling import Castling
from .square import File, Rank, Square
from .move import Move, PAWN_MOVE, PAWN_DOUBLE_MOVE, PROMOTION, CAPTURE, EP_CAPTURE, CASTLE
from .piece import PieceType, Piece, PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING


# directions

NORTH_EAST = (1, -1)
NORTH_WEST = (-1, -1)
SOUTH_EAST = (1, 1)
SOUTH_WEST = (-1, 1)

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)


# knight directions

NORTH_EAST_NORTH = (1, -2)
NORTH_EAST_EAST = (2, -1)
NORTH_WEST_NORTH = (-1, -2)
NORTH_WEST_WEST = (-2, -1)

SOUTH_EAST_SOUTH = (1, 2)
SOUTH_EAST_EAST = (2, 1)
SOUTH_WEST_SOUTH = (-1, 2)
SOUTH_WEST_WEST = (-2, 1)


pawn_directions = [SOUTH, NORTH]
piece_directions: dict[PieceType, list[tuple[int, int]]] = {
    PieceType(KNIGHT): [NORTH_EAST_NORTH, NORTH_EAST_EAST, NORTH_WEST_NORTH, NORTH_WEST_WEST,
                        SOUTH_EAST_SOUTH, SOUTH_EAST_EAST, SOUTH_WEST_SOUTH, SOUTH_WEST_WEST],
    PieceType(BISHOP): [NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST],
    PieceType(ROOK): [NORTH, SOUTH, EAST, WEST],
    PieceType(QUEEN): [NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST, NORTH, SOUTH, EAST, WEST],
    PieceType(KING): [NORTH_EAST, NORTH_WEST, SOUTH_EAST, SOUTH_WEST, NORTH, SOUTH, EAST, WEST],
}

castling_rook_info = {Square("g1"): (Square("f1"), Square("h1")), Square("c1"): (Square("d1"), Square("a1")),
                      Square("g8"): (Square("f8"), Square("h8")), Square("c8"): (Square("d8"), Square("a8"))}
castling_king_info = [
    ("kq", [Square("e8"), Square("e8")], ([Square("f8"), Square("g8")], [Square("d8"), Square("c8"), Square("b8")]),
     ([Square("e8"), Square("f8"), Square("g8")], [Square("e8"), Square("d8"), Square("c8")]), [Square("g8"), Square("c8")]),
    ("KQ", [Square("e1"), Square("e1")], ([Square("f1"), Square("g1")], [Square("d1"), Square("c1"), Square("b1")]),
     ([Square("e1"), Square("f1"), Square("g1")], [Square("e1"), Square("d1"), Square("c1")]), [Square("g1"), Square("c1")])
]


class Board:
    def __init__(self) -> None:
        self.grid: dict[Square, Piece | None]
        self.piece_squares: list[dict[PieceType, set[Square]]]

        self.clear()

    def __repr__(self) -> str:
        return f"Board('{self.string}')"

    def __str__(self) -> str:
        string = ["+-----------------+"]

        for r, rank in enumerate(Rank):
            row = ["|"]
            for file in File:
                piece = self.grid[Square(file, rank)]
                row.append("." if piece is None else piece.char)
            row.extend(["|", str(8 - r)])
            string.append(" ".join(row))

        string.append("+-----------------+")
        string.append("  a b c d e f g h")

        return "\n".join(string)

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
        ranks = string.split("/")
        if len(ranks) != 8:
            raise ValueError(f"invalid board string: '{string}'")

        grid: list[list[Piece | None]] = []
        for rank in ranks:
            grid.append([])
            for char in rank:
                if char.isdigit():
                    grid[-1].extend([None] * int(char))
                else:
                    grid[-1].append(Piece(char))

            if len(grid[-1]) != 8:
                raise ValueError(f"invalid board string: '{string}'")

        self.clear()

        for square in Square:
            piece = grid[square.rank.value][square.file.value]
            self.grid[square] = piece
            if piece is not None:
                self.piece_squares[piece.white][piece.type].add(square)

        if len(self.piece_squares[True][PieceType(KING)]) != 1 or len(self.piece_squares[False][PieceType(KING)]) != 1:
            print("warning: invalid number of kings")  # TODO Warning

    def clear(self):
        self.grid = {square: None for square in Square}
        self.piece_squares = [{type: set() for type in PieceType}, {type: set() for type in PieceType}]

    def is_attacked(self, white: bool, square: Square) -> bool:  # TODO improve, do not generate all moves
        for move in self.generate_pseudo_legal_moves(white):
            if not move.type & PAWN_MOVE and move.target == square:
                return True
        try:
            single = square + pawn_directions[not white]
        except ValueError:
            return False
        for dir in (EAST, WEST):
            try:
                target = single + dir
            except ValueError:
                continue
            piece = self.grid[target]
            if piece is not None and piece.white == white and piece.type == PAWN:
                return True
        return False

    def in_check(self, white: bool) -> bool:
        king_square_set = self.piece_squares[white][PieceType(KING)]
        if not king_square_set:
            return False
        return self.is_attacked(not white, next(iter(king_square_set)))

    def _make_piece_square(self, white: bool, move: Move):
        assert move.piece is not None
        self.piece_squares[white][move.piece.type].remove(move.source)
        if move.type & PROMOTION:
            assert move.promotion is not None
            self.piece_squares[white][move.promotion].add(move.target)
        else:
            self.piece_squares[white][move.piece.type].add(move.target)

        if move.capture is not None:
            self.piece_squares[not white][move.capture.type].remove(move.target)

    def _undo_piece_square(self, white: bool, move: Move):
        assert move.piece is not None
        self.piece_squares[white][move.piece.type].add(move.source)
        if move.type & PROMOTION:
            assert move.promotion is not None
            self.piece_squares[white][move.promotion].remove(move.target)
        else:
            self.piece_squares[white][move.piece.type].remove(move.target)

        if move.capture is not None:
            self.piece_squares[not white][move.capture.type].add(move.target)

    def make_move(self, white: bool, move: Move):
        self.grid[move.target] = Piece(white, move.promotion) if move.type & PROMOTION else move.piece
        self.grid[move.source] = None
        self._make_piece_square(white, move)

        if move.type & EP_CAPTURE:
            assert move.piece is not None
            self.grid[move.target + pawn_directions[not white]] = None
            self.piece_squares[not white][move.piece.type].remove(move.target + pawn_directions[not white])

        elif move.type & CASTLE:
            free_sqr, rook_sqr = castling_rook_info[move.target]
            self.grid[free_sqr] = self.grid[rook_sqr]
            self.grid[rook_sqr] = None
            self.piece_squares[white][PieceType(ROOK)] ^= {rook_sqr, free_sqr}

    def undo_move(self, white: bool, move: Move) -> None:
        self.grid[move.source] = Piece(white, PieceType(PAWN)) if move.type & PROMOTION else move.piece
        self.grid[move.target] = move.capture
        self._undo_piece_square(white, move)

        if move.type & EP_CAPTURE:
            assert move.piece is not None
            self.grid[move.target + pawn_directions[not white]] = Piece(not white, PieceType(PAWN))
            self.piece_squares[not white][move.piece.type].add(move.target + pawn_directions[not white])

        elif move.type & CASTLE:
            free_sqr, rook_sqr = castling_rook_info[move.target]
            self.grid[rook_sqr] = self.grid[free_sqr]
            self.grid[free_sqr] = None
            self.piece_squares[white][PieceType(ROOK)] ^= {rook_sqr, free_sqr}

    def _pawn_single_moves(self, white: bool, source: Square, target: Square, is_capture: bool) -> list[Move]:
        flags = (PAWN_MOVE | CAPTURE) if is_capture else PAWN_MOVE

        if target.rank == (Rank('8') if white else Rank('1')):
            flags |= PROMOTION
            return [Move(source, target, self, flags, prom) for prom in (KNIGHT, BISHOP, ROOK, QUEEN)]

        return [Move(source, target, self, flags, None)]

    def _pawn_forward_moves(self, white: bool, source: Square, single: Square, direction: tuple[int, int]) -> list[Move]:
        moves: list[Move] = []

        if self.grid[single] is None:
            moves.extend(self._pawn_single_moves(white, source, single, False))
            if source.rank == (Rank('2') if white else Rank('7')):
                double = single + direction
                if self.grid[double] is None:
                    moves.append(Move(source, double, self, PAWN_MOVE | PAWN_DOUBLE_MOVE, None))

        return moves

    def _pawn_capture_moves(self, white: bool, source: Square, single: Square, epsquare: Square | None) -> list[Move]:
        moves: list[Move] = []

        for dir in (EAST, WEST):
            try:
                target = single + dir
            except ValueError:
                continue
            capture = self.grid[target]
            if capture is not None and capture.white != white:
                moves.extend(self._pawn_single_moves(white, source, target, True))
            elif target == epsquare:
                moves.append(Move(source, target, self, PAWN_MOVE | CAPTURE | EP_CAPTURE, None))

        return moves

    def _pawn_moves(self, white: bool, source: Square, epsquare: Square | None) -> list[Move]:
        moves: list[Move] = []

        direction = pawn_directions[white]
        single = source + direction

        moves.extend(self._pawn_forward_moves(white, source, single, direction))
        moves.extend(self._pawn_capture_moves(white, source, single, epsquare))

        return moves

    def _piece_moves(self, white: bool, source: Square, type: PieceType) -> list[Move]:
        moves: list[Move] = []

        for direction in piece_directions[type]:
            target = source
            while True:
                try:
                    target += direction
                except ValueError:
                    break
                capture = self.grid[target]
                if capture is not None:
                    if capture.white != white:
                        moves.append(Move(source, target, self, CAPTURE, None))
                    break
                moves.append(Move(source, target, self, 0, None))
                if not type.sliding:
                    break

        return moves

    def _can_castle(self, white: bool, empty_sqrs: list[Square], no_attacked_sqrs: list[Square]) -> bool:
        for square in empty_sqrs:
            if self.grid[square] is not None:
                return False
        for square in no_attacked_sqrs:
            if self.is_attacked(not white, square):
                return False
        return True

    def _castle_moves(self, white: bool, castling: Castling) -> list[Move]:
        moves: list[Move] = []

        for flag, source, empty_sqrs, no_attacked_sqrs, target in zip(*castling_king_info[white]):
            if castling & flag and self._can_castle(white, empty_sqrs, no_attacked_sqrs):
                moves.append(Move(source, target, self, CASTLE, None))

        return moves

    def generate_pseudo_legal_moves(self, white: bool, castling: Castling = Castling(0),
                                    epsquare: Square | None = None) -> list[Move]:
        moves: list[Move] = []

        for type, squares in self.piece_squares[white].items():
            for source in squares:
                if type == PAWN:
                    moves.extend(self._pawn_moves(white, source, epsquare))
                else:
                    moves.extend(self._piece_moves(white, source, type))

        if castling & castling_king_info[white][0]:
            moves.extend(self._castle_moves(white, castling))

        return moves
