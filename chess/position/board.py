from .color import Color
from .piece import Piece
from .square import Square

from ..move.move import Move


EMPTY_BOARD_STRING = "8/8/8/8/8/8/8/8"


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

    def generate_pseudo_legal_moves(self, side: Color) -> list[Move]:
        moves = []

        for source in Square:
            if source == Square.NONE:
                continue
            if self.color[source] == side:
                if self.piece[source] == Piece.PAWN:
                    pass
                else:
                    for direction in DIRECTIONS[self.piece[source]]:
                        target = source
                        while True:
                            target += direction
                            if self.piece[target] == Piece.OFF:
                                break
                            target = Square(target)
                            if self.color[target] == Color.NONE:
                                moves.append(Move(source, target))
                                if not self.piece[target].is_sliding:
                                    break
                            else:
                                if self.color[target] != side:
                                    moves.append(Move(source, target))
                                break

        return moves
