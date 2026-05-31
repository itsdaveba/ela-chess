from collections import defaultdict

from defs import Piece, PieceType, Player, Direction, Square, Move, Rank, File


piece_movement: dict[PieceType, list[Direction]] = {
    # The bishop may move to any square along a diagonal on which it stands.
    PieceType.BISHOP: [Direction.UP_RIGHT, Direction.UP_LEFT, Direction.DOWN_LEFT, Direction.DOWN_RIGHT],
    # The rook may move to any square along the file or the rank on which it stands.
    PieceType.ROOK: [Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.DOWN],
    # The queen may move to any square along the file, the rank or a diagonal on which it stands.
    PieceType.QUEEN: [Direction.UP_RIGHT, Direction.UP_LEFT, Direction.DOWN_LEFT, Direction.DOWN_RIGHT,
                      Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.DOWN],
    PieceType.KING: []
}


class Board:
    def __init__(self) -> None:
        # The chessboard is composed of an 8 x 8 grid of 64 equal squares.
        # The initial position of the pieces on the chessboard is as follows:
        chessboard: list[list[Piece]] = [
            [Piece.BLACK_ROOK, Piece.NONE, Piece.BLACK_BISHOP, Piece.BLACK_QUEEN,
             Piece.BLACK_KING, Piece.BLACK_BISHOP, Piece.NONE, Piece.BLACK_ROOK],
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [Piece.WHITE_ROOK, Piece.NONE, Piece.WHITE_BISHOP, Piece.WHITE_QUEEN,
             Piece.WHITE_KING, Piece.WHITE_BISHOP, Piece.NONE, Piece.WHITE_ROOK]
        ]
        self.chessboard: dict[Square, Piece] = {}
        for r, rank in enumerate(chessboard):
            for f, piece in enumerate(rank):
                self.chessboard[Square(r, f)] = piece

        # The player with the white pieces commences the game.
        self.player: Player = Player.WHITE

        # TODO join attack and target_squares
        # A piece is considered to attack a square, even if such a piece is constrained from moving
        # to that square because it would then leave or place the king of its own colour under attack.
        # A piece is said to attack an opponent’s piece if the piece could
        # make a capture on that squareaccording to the Articles 3.2 to 3.8.
        self.attack: dict[Piece, dict[Square, dict[Direction, list[Square]]]] = \
            defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        self.target_squares: dict[Piece, dict[Square, set[Square]]] = defaultdict(lambda: defaultdict(set))
        self.attacked_by: dict[Square, set[tuple[Piece, Square, Direction]]] = defaultdict(set)

        for square, piece in self.chessboard.items():
            if piece is Piece.NONE:
                continue
            self.add_piece(piece, square)

        assert len(self.attack[Piece.WHITE_KING]) == 1
        assert len(self.attack[Piece.BLACK_KING]) == 1
        assert not self.king_under_attack(self.player.opponent)

    def __str__(self) -> str:
        return "\n".join([" ".join([self.chessboard[Square(r, f)].chr for f in File]) for r in Rank])

    def make_move(self, move: Move) -> bool:
        # who move their pieces alternately on a square board called a ‘chessboard’.
        source_piece = self.chessboard[move.source]
        target_piece = self.chessboard[move.target]

        if source_piece.player is not self.player:
            print(f"Player {self.player} needs to move its own piece")
            return False
        if move.source == move.target:
            print("Not permitted to move to same square")
            return False

        if source_piece.type in (PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN):
            if move.target not in self.target_squares[source_piece][move.source]:
                print(f"{move.target} not reachable by {source_piece} at {move.source}")
                return False

        # It is not permitted to move a piece to a square occupied by a piece of the same colour.
        if target_piece.player is self.player:
            print("Not permitted to move to same color")
            return False
        # and also ’capturing’ the opponent’s king are not allowed.
        if target_piece.type is PieceType.KING:
            print("Cannot capture opponent's king")
            return False

        king_was_under_attack = self.king_under_attack(self.player)

        # If a piece moves to a square occupied by an opponent’s piece
        # the latter is captured and removed from the chessboard as part of the same move.
        self.chessboard[move.target] = source_piece
        self.chessboard[move.source] = Piece.NONE

        attack, target_squares = self.remove_piece(source_piece, move.source)
        added_from, added_squares = self.add_attack(move.source)
        self.add_piece(source_piece, move.target)
        if target_piece is Piece.NONE:
            captured_attack = {}
            captured_target_squares = set()
            removed_squares = self.remove_attack(move.target)
        else:
            removed_squares = {}
            captured_attack, captured_target_squares = self.remove_piece(target_piece, move.target)

        if self.king_under_attack(self.player):
            # Leaving one’s own king under attack
            if king_was_under_attack:
                print("Cannot leave own king under attack")
            # exposing one’s own king to attack
            else:
                print("Cannot expose own king to attack")

            # unmake move
            self.chessboard[move.source] = source_piece
            self.chessboard[move.target] = target_piece

            self.remove_piece(source_piece, move.target)
            if target_piece is Piece.NONE:
                self.add_attack(move.target, removed_squares)
            else:
                self.add_piece(target_piece, move.target, captured_attack, captured_target_squares)
            self.add_piece(source_piece, move.source, attack, target_squares)
            self.remove_attack(move.source, added_from, added_squares)

            return False

        self.player = self.player.opponent
        return True

    # The objective of each player is to place the opponent’s king ‘under attack’
    def king_under_attack(self, player: Player) -> bool:
        square = next(iter(self.attack[Piece((player, PieceType.KING))]))
        # TODO separate by player
        for piece, _, _ in self.attacked_by[square]:
            if piece.player is player.opponent:
                return True
        return False

    # in such a way that the opponent has no legal move.
    def no_legal_move(self) -> bool:
        # seylf.player no legal moves
        return False

    # If the position is such that neither player can possibly checkmate, the game is drawn.
    def no_possible_checkmate(self) -> bool:
        return False

    def attack_squares(self, square: Square, direction: Direction, init_step: int = 1) -> list[Square]:
        squares = []
        square += direction * init_step
        while square.is_valid():
            squares.append(square)
            if self.chessboard[square] is not Piece.NONE:
                break
            square += direction
        return squares

    # TODO make return type a class type
    def remove_piece(self, piece: Piece, square: Square) -> tuple[dict[Direction, list[Square]], set[Square]]:
        attack = self.attack[piece].pop(square)
        target_squares = self.target_squares[piece].pop(square)
        for direction, squares in attack.items():
            for sqr in squares:
                self.attacked_by[sqr].remove((piece, square, direction))
        return attack, target_squares

    def add_piece(self, piece: Piece, square: Square,
                  attack: dict[Direction, list[Square]] = {}, target_squares: set[Square] = set()) -> None:
        if attack and target_squares:
            self.attack[piece][square] = attack
            self.target_squares[piece][square] = target_squares
            for direction, squares in attack.items():
                for sqr in squares:
                    self.attacked_by[sqr].add((piece, square, direction))
            return
        for direction in piece_movement[piece.type]:
            squares = self.attack_squares(square, direction)
            self.attack[piece][square][direction] = squares
            self.target_squares[piece][square].update(squares)
            for sqr in squares:
                self.attacked_by[sqr].add((piece, square, direction))

    def remove_attack(self, square: Square,
                      added_from: dict[tuple[Piece, Square, Direction], int] = {},
                      added_squares: dict[tuple[Piece, Square, Direction], list[Square]] = {}
                      ) -> dict[tuple[Piece, Square, Direction], list[Square]]:
        removed_squares: dict[tuple[Piece, Square, Direction], list[Square]] = {}
        if added_from and added_squares:
            for piece, sqr, direction in self.attacked_by[square]:
                remove_from = added_from[piece, sqr, direction]
                remove_squares = added_squares[piece, sqr, direction]
                self.attack[piece][sqr][direction] = self.attack[piece][sqr][direction][:remove_from]
                self.target_squares[piece][sqr].difference_update(remove_squares)
                for s in remove_squares:
                    self.attacked_by[s].remove((piece, sqr, direction))
            return removed_squares
        for piece, sqr, direction in self.attacked_by[square]:
            index = self.attack[piece][sqr][direction].index(square)
            remove_squares = self.attack[piece][sqr][direction][index + 1:]
            self.attack[piece][sqr][direction] = self.attack[piece][sqr][direction][:index + 1]
            self.target_squares[piece][sqr].difference_update(remove_squares)
            for s in remove_squares:
                self.attacked_by[s].remove((piece, sqr, direction))
            removed_squares[piece, sqr, direction] = remove_squares
        return removed_squares

    def add_attack(self, square: Square, removed_squares: dict[tuple[Piece, Square, Direction], list[Square]] = {}
                   ) -> tuple[dict[tuple[Piece, Square, Direction], int],
                              dict[tuple[Piece, Square, Direction], list[Square]]]:
        added_from: dict[tuple[Piece, Square, Direction], int] = {}
        added_squares: dict[tuple[Piece, Square, Direction], list[Square]] = {}
        if removed_squares:
            for piece, sqr, direction in self.attacked_by[square]:
                add_squares = removed_squares[piece, sqr, direction]
                self.attack[piece][sqr][direction].extend(add_squares)
                self.target_squares[piece][sqr].update(add_squares)
                for s in add_squares:
                    self.attacked_by[s].add((piece, sqr, direction))
            return added_from, added_squares
        for piece, sqr, direction in self.attacked_by[square]:
            add_from = len(self.attack[piece][sqr][direction])
            add_squares = self.attack_squares(sqr, direction, add_from + 1)
            self.attack[piece][sqr][direction].extend(add_squares)
            self.target_squares[piece][sqr].update(add_squares)
            for s in add_squares:
                self.attacked_by[s].add((piece, sqr, direction))
            added_from[piece, sqr, direction] = add_from
            added_squares[piece, sqr, direction] = add_squares
        return added_from, added_squares
