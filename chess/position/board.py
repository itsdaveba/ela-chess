from .color import Color
from .piece import Piece
from .castling import Castling
from .square import Square, Rank, NUM_SQUARES

from ..move.move import Move, MoveType


EMPTY_BOARD_STRING: str = "8/8/8/8/8/8/8/8"
SECOND_RANK: list[Rank] = [Rank.R2, Rank.R7]
PIECES: list[Piece] = [Piece.PAWN, Piece.KNIGHT, Piece.BISHOP, Piece.ROOK, Piece.QUEEN, Piece.KING]

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
CASTLING_ROOK_INFO: list[dict[Square, tuple[Square, Square]]] = [
    {Square.G1: (Square.H1, Square.F1), Square.C1: (Square.A1, Square.D1)},
    {Square.G8: (Square.H8, Square.F8), Square.C8: (Square.A8, Square.D8)}
]

PAWN_FORWARD: list[list[Square]] = [[Square.NONE] * NUM_SQUARES, [Square.NONE] * NUM_SQUARES]
ATTACK_SQUARES = [[[] for _ in range(NUM_SQUARES)] for _ in PIECES]
ATTACK_SQUARES[Piece.PAWN] = [[[] for _ in range(NUM_SQUARES)], [[] for _ in range(NUM_SQUARES)]]

squares = list(Square)
BIG_BOARD: list[Square] = []
for r in range(8):
    BIG_BOARD.append(Square.NONE)
    BIG_BOARD.extend(squares[r * 8:r * 8 + 8])
    BIG_BOARD.append(Square.NONE)
BIG_BOARD.extend([Square.NONE] * 20)

TO_BIG_BOARD: list[int] = []
for r in range(8):
    TO_BIG_BOARD.extend([f for f in range(r * 10 + 1, r * 10 + 9)])

for origin in Square:
    if origin == Square.NONE:
        continue
    for piece in PIECES:
        if piece == Piece.PAWN:
            for color in (Color.WHITE, Color.BLACK):
                single = TO_BIG_BOARD[origin] + DIRECTIONS[Piece.PAWN][color]
                if BIG_BOARD[single] != Square.NONE:
                    PAWN_FORWARD[color][origin] = BIG_BOARD[single]
                    for target in (single - 1, single + 1):
                        if BIG_BOARD[target] != Square.NONE:
                            ATTACK_SQUARES[Piece.PAWN][color][origin].append(BIG_BOARD[target])
            continue
        for d, direction in enumerate(DIRECTIONS[piece]):
            squares = []
            target = TO_BIG_BOARD[origin]
            while True:
                target += direction
                if BIG_BOARD[target] == Square.NONE:
                    break
                if not piece.is_sliding:
                    ATTACK_SQUARES[piece][origin].append(BIG_BOARD[target])
                    break
                squares.append(BIG_BOARD[target])
            if piece.is_sliding and squares:
                ATTACK_SQUARES[piece][origin].append(squares)


class Board:
    def __init__(self, string: str = EMPTY_BOARD_STRING) -> None:
        self.color: list[Color]
        self.piece: list[Piece]
        self.piece_list: list[list[set[Square]]]

        self.string = string

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

        ranks = string.split("/")
        if len(ranks) != 8:
            raise ValueError(f"invalid board string: '{string}'")

        square = Square.A8.value
        for rank in ranks:
            for char in rank:
                if char.isdigit():
                    square += int(char)
                else:
                    self.color[square] = Color.WHITE if char.isupper() else Color.BLACK
                    self.piece[square] = Piece.from_char(char.upper())
                    self.piece_list[self.color[square]][self.piece[square]].add(Square(square))
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
                    moves.append(Move(origin, target, MoveType.NONE))
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

        if capture != Piece.NONE:
            self.piece_list[side.opponent][capture].remove(move.target)

        self.color[move.target] = side
        if move.type & MoveType.PROMOTION:
            self.piece[move.target] = move.promotion
            self.piece_list[side][move.promotion].add(move.target)
        else:
            self.piece[move.target] = piece
            self.piece_list[side][piece].add(move.target)

        self.color[move.origin] = Color.NONE
        self.piece[move.origin] = Piece.NONE
        self.piece_list[side][piece].remove(move.origin)

        if move.type & MoveType.EPCAPTURE:
            target = PAWN_FORWARD[side.opponent][move.target]
            self.color[target] = Color.NONE
            self.piece[target] = Piece.NONE
            self.piece_list[side.opponent][Piece.PAWN].remove(target)

        if move.type & MoveType.CASTLE:
            origin, target = CASTLING_ROOK_INFO[side][move.target]

            self.color[target] = side
            self.piece[target] = Piece.ROOK
            self.piece_list[side][Piece.ROOK].add(target)

            self.color[origin] = Color.NONE
            self.piece[origin] = Piece.NONE
            self.piece_list[side][Piece.ROOK].remove(origin)

        return capture

    def undo_move(self, side: Color, move: Move, capture: Piece) -> None:
        piece = self.piece[move.target]

        self.color[move.origin] = side
        if move.type & MoveType.PROMOTION:
            self.piece[move.origin] = Piece.PAWN
            self.piece_list[side][Piece.PAWN].add(move.origin)
        else:
            self.piece[move.origin] = piece
            self.piece_list[side][piece].add(move.origin)

        if capture != Piece.NONE:
            self.color[move.target] = side.opponent
            self.piece_list[side.opponent][capture].add(move.target)
        else:
            self.color[move.target] = Color.NONE
        self.piece[move.target] = capture
        self.piece_list[side][piece].remove(move.target)

        if move.type & MoveType.EPCAPTURE:
            target = PAWN_FORWARD[side.opponent][move.target]
            self.color[target] = side.opponent
            self.piece[target] = Piece.PAWN
            self.piece_list[side.opponent][Piece.PAWN].add(target)

        if move.type & MoveType.CASTLE:
            origin, target = CASTLING_ROOK_INFO[side][move.target]

            self.color[origin] = side
            self.piece[origin] = Piece.ROOK
            self.piece_list[side][Piece.ROOK].add(origin)

            self.color[target] = Color.NONE
            self.piece[target] = Piece.NONE
            self.piece_list[side][Piece.ROOK].remove(target)
