import random

from .color import Color
from .piece import Piece
from .castling import Castling
from .square import Square, Rank, NUM_SQUARES

from ..move.move import Move, MoveType


EMPTY_BOARD_STRING: str = "8/8/8/8/8/8/8/8"
SECOND_RANK: list[Rank] = [Rank.R2, Rank.R7]
PIECES: list[Piece] = [Piece.PAWN, Piece.KNIGHT, Piece.BISHOP, Piece.ROOK, Piece.QUEEN, Piece.KING]

DIRECTIONS: list[list[int]] = [
    [-16, 16],  # pawn
    [-33, -31, -18, -14, 14, 18, 31, 33],  # knight
    [-17, -15, 15, 17],  # bishop
    [-16, -1, 1, 16],  # rook
    [-17, -16, -15, -1, 1, 15, 16, 17],  # queen
    [-17, -16, -15, -1, 1, 15, 16, 17]  # king
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
CASTLING_ROOK_INFO: list[dict[Square, tuple[Square, Square]]] = [
    {Square.G1: (Square.H1, Square.F1), Square.C1: (Square.A1, Square.D1)},
    {Square.G8: (Square.H8, Square.F8), Square.C8: (Square.A8, Square.D8)}
]

PAWN_FORWARD: list[list[Square]] = [[Square.NONE] * NUM_SQUARES, [Square.NONE] * NUM_SQUARES]
ATTACK_SQUARES = [[[] for _ in range(NUM_SQUARES)] for _ in PIECES]
ATTACK_SQUARES[Piece.PAWN] = [[[] for _ in range(NUM_SQUARES)], [[] for _ in range(NUM_SQUARES)]]

squares = list(Square)
BOARD_0X88: list[Square] = []
for r in range(8):
    BOARD_0X88.extend(squares[r * 8:r * 8 + 8])
    BOARD_0X88.extend([Square.NONE] * 8)

TO_BOARD_0X88: list[int] = []
for r in range(8):
    TO_BOARD_0X88.extend([f for f in range(r * 16, r * 16 + 8)])

PIECE_VALUE: list[int] = [100, 320, 330, 500, 900, 20000]
PIECE_TABLE: list[list[int]] = [
    [  # pawn
        0,   0,   0,   0,   0,   0,   0,   0,
        50, 50,  50,  50,  50,  50,  50,  50,
        10, 10,  20,  30,  30,  20,  10,  10,
        5,   5,  10,  25,  25,  10,   5,   5,
        0,   0,   0,  20,  20,   0,   0,   0,
        5,  -5, -10,   0,   0, -10,  -5,   5,
        5,  10,  10, -20, -20,  10,  10,   5,
        0,   0,   0,   0,   0,   0,   0,   0
    ],
    [  # knight
        -50, -40, -30, -30, -30, -30, -40, -50,
        -40, -20,   0,   0,   0,   0, -20, -40,
        -30,   0,  10,  15,  15,  10,   0, -30,
        -30,   5,  15,  20,  20,  15,   5, -30,
        -30,   0,  15,  20,  20,  15,   0, -30,
        -30,   5,  10,  15,  15,  10,   5, -30,
        -40, -20,   0,   5,   5,   0, -20, -40,
        -50, -40, -30, -30, -30, -30, -40, -50
    ],
    [  # bishop
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10,   0,   0,   0,   0,   0,   0, -10,
        -10,   0,   5,  10,  10,   5,   0, -10,
        -10,   5,   5,  10,  10,   5,   5, -10,
        -10,   0,  10,  10,  10,  10,   0, -10,
        -10,  10,  10,  10,  10,  10,  10, -10,
        -10,   5,   0,   0,   0,   0,   5, -10,
        -20, -10, -10, -10, -10, -10, -10, -20
    ],
    [  # rook
        0,   0,  0,  0,  0,  0,  0,  0,
        5,  10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        0,   0,  0,  5,  5,  0,  0,  0
    ],
    [  # queen
        -20, -10, -10,  -5,  -5, -10, -10, -20,
        -10,   0,   0,   0,   0,   0,   0, -10,
        -10,   0,   5,   5,   5,   5,   0, -10,
        -5,    0,   5,   5,   5,   5,   0,  -5,
        0,     0,   5,   5,   5,   5,   0,  -5,
        -10,   5,   5,   5,   5,   5,   0, -10,
        -10,   0,   5,   0,   0,   0,   0, -10,
        -20, -10, -10,  -5,  -5, -10, -10, -20
    ],
    [  # king
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        20,   20,   0,   0,   0,   0,  20,  20,
        20,   30,  10,   0,   0,  10,  30,  20
    ]
]

PIECE_SQUARE_VALUE: list[list[list[int]]] = [[[0] * NUM_SQUARES for _ in PIECES], [[0] * NUM_SQUARES for _ in PIECES]]
HASH_VALUE: list[list[list[int]]] = [[[0] * NUM_SQUARES for _ in PIECES], [[0] * NUM_SQUARES for _ in PIECES]]

for origin in Square:
    if origin == Square.NONE:
        continue
    for piece in PIECES:
        if piece == Piece.PAWN:
            for color in (Color.WHITE, Color.BLACK):
                single = TO_BOARD_0X88[origin] + DIRECTIONS[Piece.PAWN][color]
                if not single & 0x88:
                    PAWN_FORWARD[color][origin] = BOARD_0X88[single]
                    for target in (single - 1, single + 1):
                        if not target & 0x88:
                            ATTACK_SQUARES[Piece.PAWN][color][origin].append(BOARD_0X88[target])
        else:
            for d, direction in enumerate(DIRECTIONS[piece]):
                squares = []
                target = TO_BOARD_0X88[origin]
                while True:
                    target += direction
                    if target & 0x88:
                        break
                    if not piece.is_sliding:
                        ATTACK_SQUARES[piece][origin].append(BOARD_0X88[target])
                        break
                    squares.append(BOARD_0X88[target])
                if piece.is_sliding and squares:
                    ATTACK_SQUARES[piece][origin].append(squares)

        value = PIECE_VALUE[piece]
        table = PIECE_TABLE[piece]
        PIECE_SQUARE_VALUE[Color.WHITE][piece][origin] = value + table[origin.rank * 8 + origin.file]
        PIECE_SQUARE_VALUE[Color.BLACK][piece][origin] = -value - table[(7 - origin.rank) * 8 + origin.file]

        HASH_VALUE[Color.WHITE][piece][origin] = random.getrandbits(64)
        HASH_VALUE[Color.BLACK][piece][origin] = random.getrandbits(64)


class Board:
    def __init__(self, string: str = EMPTY_BOARD_STRING) -> None:
        self.color: list[Color]
        self.piece: list[Piece]
        self.piece_list: list[list[set[Square]]]
        self.eval: int
        self.hash: int

        self.string = string

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Board):
            return self.hash == other.hash
        return False

    def __repr__(self) -> str:
        return self.string

    def __str__(self) -> str:
        ranks = []

        for r in range(8):
            rank = []
            color_rank = self.color[r * 8:]
            piece_rank = self.piece[r * 8:]
            for f in range(8):
                rank.append(piece_rank[f].char.lower() if color_rank[f] == Color.BLACK else piece_rank[f].char)
            ranks.append(" ".join(rank))

        return "\n".join(ranks)

    @property
    def string(self) -> str:
        ranks = []

        for r in range(8):
            rank = ""
            count = 0
            color_rank = self.color[r * 8:]
            piece_rank = self.piece[r * 8:]
            for f in range(8):
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
        self.color = [Color.NONE] * NUM_SQUARES
        self.piece = [Piece.NONE] * NUM_SQUARES
        self.piece_list = [[set() for _ in PIECES], [set() for _ in PIECES]]
        self.eval = 0
        self.hash = 0

        ranks = string.split("/")
        if len(ranks) != 8:
            raise ValueError(f"invalid board string: '{string}'")

        square = Square.A8.value
        for rank in ranks:
            for char in rank:
                if char.isdigit():
                    square += int(char)
                else:
                    self._add_piece(Color.WHITE if char.isupper() else Color.BLACK,
                                    Piece.from_char(char.upper()), Square(square))
                    square += 1
            if square % 8 != 0:
                raise ValueError(f"invalid board string: '{string}'")

    def is_attacked(self, square: Square, side: Color) -> bool:
        # pawn attacks
        for target in ATTACK_SQUARES[Piece.PAWN][side.opponent][square]:
            if self.color[target] == side and self.piece[target] == Piece.PAWN:
                return True

        # knight attacks
        for target in ATTACK_SQUARES[Piece.KNIGHT][square]:
            if self.color[target] == side and self.piece[target] == Piece.KNIGHT:
                return True

        # bishop attacks
        for direction in ATTACK_SQUARES[Piece.BISHOP][square]:
            target = direction[0]
            if self.color[target] != Color.NONE:
                if self.color[target] == side and self.piece[target] in (Piece.BISHOP, Piece.QUEEN, Piece.KING):
                    return True
                continue
            for target in direction[1:]:
                if self.color[target] != Color.NONE:
                    if self.color[target] == side and self.piece[target] in (Piece.BISHOP, Piece.QUEEN):
                        return True
                    break

        # rook attacks
        for direction in ATTACK_SQUARES[Piece.ROOK][square]:
            target = direction[0]
            if self.color[target] != Color.NONE:
                if self.color[target] == side and self.piece[target] in (Piece.ROOK, Piece.QUEEN, Piece.KING):
                    return True
                continue
            for target in direction[1:]:
                if self.color[target] != Color.NONE:
                    if self.color[target] == side and self.piece[target] in (Piece.ROOK, Piece.QUEEN):
                        return True
                    break

        return False

    def in_check(self, side: Color) -> bool:
        if self.piece_list[side][Piece.KING]:
            return self.is_attacked(next(iter(self.piece_list[side][Piece.KING])), side.opponent)
        return False

    def generate_pseudo_legal_moves(self, side: Color, castling: Castling, epsquare: Square) -> list[Move]:
        moves = []

        for piece, squares in zip(PIECES, self.piece_list[side]):
            for origin in squares:
                if piece == Piece.PAWN:
                    moves.extend(self._pawn_moves(side, origin, epsquare))
                else:
                    moves.extend(self._piece_moves(side, piece, origin))
                    if piece == Piece.KING and castling & CASTLING_FLAGS[side]:
                        moves.extend(self._castle_moves(side, origin, castling))

        return moves

    def _pawn_moves(self, side: Color, origin: Square, epsquare: Square) -> list[Move]:
        moves = []

        moves.extend(self._pawn_forward_moves(side, origin))
        moves.extend(self._pawn_capture_moves(side, origin, epsquare))

        return moves

    def _pawn_forward_moves(self, side: Color, origin: Square) -> list[Move]:
        moves = []

        type = MoveType.PAWN_MOVE
        single = PAWN_FORWARD[side][origin]
        if self.piece[single] == Piece.NONE:
            moves.extend(self._maybe_promotion_moves(side, origin, single, type))
            if origin.rank == SECOND_RANK[side]:
                double = PAWN_FORWARD[side][single]
                if self.piece[double] == Piece.NONE:
                    moves.append(Move(origin, double, type | MoveType.PAWN_DOUBLE_MOVE))

        return moves

    def _pawn_capture_moves(self, side: Color, origin: Square, epsquare: Square) -> list[Move]:
        moves = []

        type = MoveType.PAWN_MOVE | MoveType.CAPTURE
        for target in ATTACK_SQUARES[Piece.PAWN][side][origin]:
            if self.color[target] == Color.NONE:
                if target == epsquare:
                    moves.append(Move(origin, target, type | MoveType.EPCAPTURE))
            elif self.color[target] != side:
                moves.extend(self._maybe_promotion_moves(side, origin, target, type))

        return moves

    def _maybe_promotion_moves(self, side: Color, origin: Square, target: Square, type: MoveType) -> list[Move]:
        if origin.rank == SECOND_RANK[side.opponent]:
            moves = []
            for promotion in (Piece.KNIGHT, Piece.BISHOP, Piece.ROOK, Piece.QUEEN):
                moves.append(Move(origin, target, type | MoveType.PROMOTION, promotion))
            return moves
        return [Move(origin, target, type)]

    def _piece_moves(self, side: Color, piece: Piece, origin: Square) -> list[Move]:
        moves = []

        is_sliding = piece.is_sliding
        directions = ATTACK_SQUARES[piece][origin] if is_sliding else [ATTACK_SQUARES[piece][origin]]
        for direction in directions:
            for target in direction:
                if self.color[target] == Color.NONE:
                    moves.append(Move(origin, target, MoveType.NORMAL))
                    continue
                if self.color[target] != side:
                    moves.append(Move(origin, target, MoveType.CAPTURE))
                if is_sliding:
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
        piece = self.piece[move.origin]
        capture = self.piece[move.target]

        self._remove_piece(side, piece, move.origin)
        if capture != Piece.NONE:
            self._replace_piece(side.opponent, capture, side,
                                move.promotion if move.type & MoveType.PROMOTION else piece, move.target)
        else:
            self._add_piece(side, move.promotion if move.type & MoveType.PROMOTION else piece, move.target)

        if move.type & MoveType.EPCAPTURE:
            self._remove_piece(side.opponent, Piece.PAWN, PAWN_FORWARD[side.opponent][move.target])

        if move.type & MoveType.CASTLE:
            origin, target = CASTLING_ROOK_INFO[side][move.target]
            self._remove_piece(side, Piece.ROOK, origin)
            self._add_piece(side, Piece.ROOK, target)

        return capture

    def undo_move(self, side: Color, move: Move, capture: Piece) -> None:
        piece = self.piece[move.target]

        if capture != Piece.NONE:
            self._replace_piece(side, piece, side.opponent, capture, move.target)
        else:
            self._remove_piece(side, piece, move.target)
        self._add_piece(side, Piece.PAWN if move.type & MoveType.PROMOTION else piece, move.origin)

        if move.type & MoveType.EPCAPTURE:
            self._add_piece(side.opponent, Piece.PAWN, PAWN_FORWARD[side.opponent][move.target])

        if move.type & MoveType.CASTLE:
            origin, target = CASTLING_ROOK_INFO[side][move.target]
            self._remove_piece(side, Piece.ROOK, target)
            self._add_piece(side, Piece.ROOK, origin)

    def _add_piece(self, side: Color, piece: Piece, square: Square) -> None:
        self.color[square] = side
        self.piece[square] = piece
        self.piece_list[side][piece].add(square)
        self.eval += PIECE_SQUARE_VALUE[side][piece][square]
        self.hash ^= HASH_VALUE[side][piece][square]

    def _remove_piece(self, side: Color, piece: Piece, square: Square) -> None:
        self.color[square] = Color.NONE
        self.piece[square] = Piece.NONE
        self.piece_list[side][piece].remove(square)
        self.eval -= PIECE_SQUARE_VALUE[side][piece][square]
        self.hash ^= HASH_VALUE[side][piece][square]

    def _replace_piece(self, old_side: Color, old_piece: Piece,
                       new_side: Color, new_piece: Piece, square: Square) -> None:
        self.color[square] = new_side
        self.piece[square] = new_piece
        self.piece_list[old_side][old_piece].remove(square)
        self.piece_list[new_side][new_piece].add(square)
        self.eval += PIECE_SQUARE_VALUE[new_side][new_piece][square] - PIECE_SQUARE_VALUE[old_side][old_piece][square]
        self.hash ^= HASH_VALUE[new_side][new_piece][square] ^ HASH_VALUE[old_side][old_piece][square]
