from .piece import Piece
from .color import Color


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
            color_rank = self.color[r * 8:]
            piece_rank = self.piece[r * 8:]
            for f in range(8):
                piece = piece_rank[f]
                char = piece.char
                rank.append(char if color_rank[f] == Color.WHITE else char.lower())
            ranks.append(" ".join(rank))

        return "\n".join(ranks)

    @property
    def string(self) -> str:
        ranks = []

        for r in range(8):
            rank = ""
            count = 0
            for f in range(8):
                piece = self.piece[r * 8 + f]
                if piece == Piece.NONE:
                    count += 1
                    continue
                if count:
                    rank += str(count)
                    count = 0
                rank += piece.char if self.color[r * 8 + f] == Color.WHITE else piece.char.lower()
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
            color_rank = []
            piece_rank = []
            for char in rank:
                if char.isdigit():
                    color_rank.extend([Color.WHITE] * int(char))
                    piece_rank.extend([Piece.NONE] * int(char))
                else:
                    color_rank.append(Color.WHITE if char.isupper() else Color.BLACK)
                    piece_rank.append(Piece.from_char(char.upper()))
            if len(piece_rank) != 8:
                raise ValueError(f"invalid board string: '{string}'")

            self.color.extend(color_rank)
            self.piece.extend(piece_rank)
