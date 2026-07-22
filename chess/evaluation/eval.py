from ..position.color import Color
from ..position.piece import Piece
from ..position.position import Position
from ..position.square import Square, File, Rank


BOARD_SIZE: int = 100

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

PIECE_SQUARE_VALUE: list[list[list[int]]] = [[[0] * BOARD_SIZE for _ in Piece] for _ in Color]

for piece, table in zip(Piece, PIECE_TABLE):
    square_iter = iter(Square)
    for rank in Rank:
        if rank == Rank.NONE:
            continue
        for file in File:
            if file == File.NONE:
                continue
            square = next(square_iter)
            PIECE_SQUARE_VALUE[Color.WHITE][piece][square] = PIECE_VALUE[piece] + table[rank * 8 + file]
            PIECE_SQUARE_VALUE[Color.BLACK][piece][square] = PIECE_VALUE[piece] + table[(7 - rank) * 8 + file]


def evaluate(position: Position) -> int:
    eval = 0
    side = position.side

    for square in Square:
        color = position.board.color[square]
        piece = position.board.piece[square]
        if color != Color.NONE:
            value = PIECE_SQUARE_VALUE[color][piece][square]
            eval += value if color == side else -value

    return eval
