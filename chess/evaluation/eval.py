from ..position.position import Position, Square, Color, Piece


PIECE_VALUE: list[int] = [100, 300, 300, 500, 900]


def evaluate(position: Position) -> int:
    eval = 0
    side = position.side

    for square in Square:
        color = position.board.color[square]
        piece = position.board.piece[square]
        if color != Color.NONE and piece != Piece.KING:
            value = PIECE_VALUE[piece]
            eval += value if color == side else -value

    return eval
