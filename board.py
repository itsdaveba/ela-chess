from collections import defaultdict

from defs import Piece, PieceType, Player, Direction, Square, Move, Rank, File


piece_attack: dict[PieceType, list[Direction]] = {
    # The bishop may move to any square along a diagonal on which it stands.
    PieceType.BISHOP: [Direction.UP_RIGHT, Direction.UP_LEFT, Direction.DOWN_LEFT, Direction.DOWN_RIGHT],
    # The rook may move to any square along the file or the rank on which it stands.
    PieceType.ROOK: [Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.DOWN],
    # The queen may move to any square along the file, the rank or a diagonal on which it stands.
    PieceType.QUEEN: [Direction.RIGHT, Direction.UP_RIGHT, Direction.UP, Direction.UP_LEFT,
                      Direction.LEFT, Direction.DOWN_LEFT, Direction.DOWN, Direction.DOWN_RIGHT],
    # The knight may move to one of the squares nearest to that on which it stands but not on the same rank, file or diagonal.
    PieceType.KNIGHT: [Direction.RIGHT_RIGHT_UP, Direction.UP_UP_RIGHT,
                       Direction.UP_UP_LEFT, Direction.LEFT_LEFT_UP,
                       Direction.LEFT_LEFT_DOWN, Direction.DOWN_DOWN_LEFT,
                       Direction.DOWN_DOWN_RIGHT, Direction.RIGHT_RIGHT_DOWN],
    PieceType.KING: []
}

attack_table: dict[tuple[PieceType, Square], set[Square]] = defaultdict(set)
attack_pawn_table: dict[tuple[Player, Square], set[Square]] = defaultdict(set)
attack_sliding_table: dict[tuple[PieceType, Square, Direction], list[Square]] = defaultdict(list)

for type in PieceType:
    if type is PieceType.NONE:
        continue
    for r in range(8):
        for f in range(8):
            square = Square(r, f)
            if type is PieceType.PAWN:
                if square.file == File.F0:
                    attack_pawn_table[Player.WHITE, square].add(square + Direction.UP_RIGHT)
                    attack_pawn_table[Player.BLACK, square].add(square + Direction.DOWN_RIGHT)
                elif square.file == File.F7:
                    attack_pawn_table[Player.WHITE, square].add(square + Direction.UP_LEFT)
                    attack_pawn_table[Player.BLACK, square].add(square + Direction.DOWN_LEFT)
                else:
                    attack_pawn_table[Player.WHITE, square].add(square + Direction.UP_RIGHT)
                    attack_pawn_table[Player.BLACK, square].add(square + Direction.DOWN_RIGHT)
                    attack_pawn_table[Player.WHITE, square].add(square + Direction.UP_LEFT)
                    attack_pawn_table[Player.BLACK, square].add(square + Direction.DOWN_LEFT)
                continue
            for direction in piece_attack[type]:
                sqr = square + direction
                while sqr.is_valid():
                    if type.is_sliding:
                        attack_sliding_table[type, square, direction].append(sqr)
                    else:
                        attack_table[type, square].add(sqr)
                        break
                    sqr += direction


class Board:
    def __init__(self) -> None:
        # The chessboard is composed of an 8 x 8 grid of 64 equal squares.
        # The initial position of the pieces on the chessboard is as follows:
        chessboard: list[list[Piece]] = [
            [Piece.BLACK_ROOK, Piece.BLACK_KNIGHT, Piece.BLACK_BISHOP, Piece.BLACK_QUEEN,
             Piece.BLACK_KING, Piece.BLACK_BISHOP, Piece.BLACK_KNIGHT, Piece.BLACK_ROOK],
            [Piece.BLACK_PAWN] * 8,
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [Piece.NONE] * 8,
            [Piece.WHITE_PAWN] * 8,
            [Piece.WHITE_ROOK, Piece.WHITE_KNIGHT, Piece.WHITE_BISHOP, Piece.WHITE_QUEEN,
             Piece.WHITE_KING, Piece.WHITE_BISHOP, Piece.WHITE_KNIGHT, Piece.WHITE_ROOK]
        ]
        self.chessboard: dict[Square, Piece] = {}
        for r, rank in enumerate(chessboard):
            for f, piece in enumerate(rank):
                self.chessboard[Square(r, f)] = piece

        # The player with the white pieces commences the game.
        self.player: Player = Player.WHITE
        self.ep_square: Square | None = None  # TODO update to Square.NONE

        # A piece is considered to attack a square, even if such a piece is constrained from moving
        # to that square because it would then leave or place the king of its own colour under attack.
        # A piece is said to attack an opponent’s piece if the piece could
        # make a capture on that squareaccording to the Articles 3.2 to 3.8.
        self.attack: dict[Piece, dict[Square, set[Square]]] = defaultdict(lambda: defaultdict(set))
        self.attack_sliding: dict[Piece, dict[Square, dict[Direction, list[Square]]]] = \
            defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        self.attacked_by: dict[Square, dict[Player, set[tuple[PieceType, Square]]]] = defaultdict(lambda: defaultdict(set))
        self.attacked_by_sliding: dict[Square, dict[Player, set[tuple[PieceType, Square, Direction]]]] = \
            defaultdict(lambda: defaultdict(set))

        for square, piece in self.chessboard.items():
            if piece is Piece.NONE:
                continue
            self.add_piece(piece, square)

        assert len(self.attack[Piece.WHITE_KING]) == 1
        assert len(self.attack[Piece.BLACK_KING]) == 1
        assert all([square.rank != Rank.R0 and square.rank != Rank.R7 for square in self.attack[Piece.WHITE_PAWN]])
        assert all([square.rank != Rank.R0 and square.rank != Rank.R7 for square in self.attack[Piece.BLACK_PAWN]])
        assert not self.king_under_attack(self.player.opponent)

    def __str__(self) -> str:
        return "\n".join([" ".join([self.chessboard[Square(r, f)].chr for f in File]) for r in Rank])

    def make_move(self, move: Move) -> bool:
        # who move their pieces alternately on a square board called a ‘chessboard’.
        source_piece = self.chessboard[move.source]
        target_piece = self.chessboard[move.target]

        prev_ep_square = self.ep_square
        ep_square = None
        ep_capture = False
        ep_capture_square = None  # TODO update
        ep_capture_piece = Piece.NONE

        promotion = False
        promotion_piece = Piece.NONE

        if source_piece.player is not self.player:
            print(f"Player {self.player} needs to move its own piece")
            return False
        if move.source == move.target:
            print("Not permitted to move to same square")
            return False

        if move.promotion is not PieceType.NONE:
            if source_piece.type is not PieceType.PAWN:
                print("Only pawns can promote")
                return False
            last_rank = Rank.R0 if self.player is Player.WHITE else Rank.R7
            if move.target.rank != last_rank:
                print("Can't promote")
                return False
            promotion = True
            promotion_piece = Piece((self.player, move.promotion))

        if source_piece.type is PieceType.PAWN and move.target.file == move.source.file:
            # The pawn may move forward to the unoccupied square immediately in front of it on the same file, or
            first_move = move.source.rank == Rank.R6 if self.player is Player.WHITE else move.source.rank == Rank.R1
            direction = Direction.UP if self.player is Player.WHITE else Direction.DOWN
            single = move.source + direction
            if self.chessboard[single] is not Piece.NONE:
                print(f"{move.target} not reachable by {source_piece} at {move.source}")
                return False
            if first_move:
                # on its first move the pawn may move as in 3.7.a or alternatively it may
                # advance two squares along the same file provided both squares are unoccupied, or
                double = single + direction
                if move.target != single and move.target != double:
                    print(f"{move.target} not reachable by {source_piece} at {move.source}")
                    return False
                if move.target == double:
                    if self.chessboard[double] is not Piece.NONE:
                        print(f"{move.target} not reachable by {source_piece} at {move.source}")
                        return False
                    ep_square = single
            elif move.target != single:
                print(f"{move.target} not reachable by {source_piece} at {move.source}")
                return False
        else:
            if move.target not in self.attack[source_piece][move.source]:
                print(f"{move.target} not reachable by {source_piece} at {move.source}")
                return False
            if source_piece.type is PieceType.PAWN:
                # the pawn may move to a square occupied by an opponent’s piece, which
                # is diagonally in front of it on an adjacent file, capturing that piece.
                if target_piece is Piece.NONE:
                    # A pawn attacking a square crossed by an opponent’s pawn which has advanced two squares
                    # in one move from its original square may capture this opponent’s pawn as though the latter
                    # had been moved only one square. This capture is only legal on the move following this advance
                    # and is called an ‘en passant’ capture.
                    if move.target != self.ep_square:
                        print(f"{move.target} not reachable by {source_piece} at {move.source}")
                        return False
                    ep_capture = True

        # It is not permitted to move a piece to a square occupied by a piece of the same colour.
        if target_piece.player is self.player:
            print("Not permitted to move to same color")
            return False
        # and also ’capturing’ the opponent’s king are not allowed.
        if target_piece.type is PieceType.KING:
            print("Cannot capture opponent's king")
            return False

        king_was_under_attack = self.king_under_attack(self.player)

        if promotion:
            # When a pawn reaches the rank furthest from its starting position it must be
            # exchanged as part of the same move on the same square for a new queen, rook,
            # bishop or knight of the same colour. The player’s choice is not restricted to pieces
            # that have been captured previously. This exchange of a pawn for another piece is
            # called ‘promotion’ and the effect of the new piece is immediate
            self.chessboard[move.target] = promotion_piece
        else:
            # If a piece moves to a square occupied by an opponent’s piece
            # the latter is captured and removed from the chessboard as part of the same move.
            self.chessboard[move.target] = source_piece
        self.chessboard[move.source] = Piece.NONE
        if ep_capture:
            ep_capture_piece = Piece.BLACK_PAWN if self.player is Player.WHITE else Piece.WHITE_PAWN
            ep_capture_square = move.target + Direction.DOWN if self.player is Player.WHITE else move.target + Direction.UP
            self.chessboard[ep_capture_square] = Piece.NONE
            self.remove_piece(ep_capture_piece, ep_capture_square)
            self.add_slide_attack(ep_capture_square)

        self.ep_square = ep_square

        self.remove_piece(source_piece, move.source)
        self.add_slide_attack(move.source)
        self.add_piece(promotion_piece if promotion else source_piece, move.target)
        if target_piece is Piece.NONE:
            self.remove_slide_attack(move.target)
        else:
            self.remove_piece(target_piece, move.target)

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
            if ep_capture:
                self.chessboard[ep_capture_square] = ep_capture_piece
                self.add_piece(ep_capture_piece, ep_capture_square)
                self.remove_slide_attack(ep_capture_square)

            self.ep_square = prev_ep_square

            self.remove_piece(promotion_piece if promotion else source_piece, move.target)
            if target_piece is Piece.NONE:
                self.add_slide_attack(move.target)
            else:
                self.add_piece(target_piece, move.target)
            self.add_piece(source_piece, move.source)
            self.remove_slide_attack(move.source)

            return False

        self.player = self.player.opponent
        return True

    # The objective of each player is to place the opponent’s king ‘under attack’
    def king_under_attack(self, player: Player) -> bool:
        square = next(iter(self.attack[Piece((player, PieceType.KING))]))
        if self.attacked_by_sliding[square][player.opponent]:
            return True
        return bool(self.attacked_by[square][player.opponent])

    # in such a way that the opponent has no legal move.
    def no_legal_move(self) -> bool:
        # seylf.player no legal moves
        return False

    # If the position is such that neither player can possibly checkmate, the game is drawn.
    def no_possible_checkmate(self) -> bool:
        return False

    def remove_piece(self, piece: Piece, square: Square) -> None:
        attack = self.attack[piece].pop(square)
        if piece.type.is_sliding:
            for direction, squares in self.attack_sliding[piece].pop(square).items():
                for sqr in squares:
                    self.attacked_by_sliding[sqr][piece.player].remove((piece.type, square, direction))
            return
        for sqr in attack:
            self.attacked_by[sqr][piece.player].remove((piece.type, square))

    def add_piece(self, piece: Piece, square: Square) -> None:
        if piece.type.is_sliding:
            for direction in piece_attack[piece.type]:
                for sqr in attack_sliding_table[piece.type, square, direction]:
                    self.attack[piece][square].add(sqr)
                    self.attack_sliding[piece][square][direction].append(sqr)
                    self.attacked_by_sliding[sqr][piece.player].add((piece.type, square, direction))
                    if self.chessboard[sqr] is not Piece.NONE:
                        break
            return
        if piece.type is PieceType.KING:  # TODO remove
            self.attack[piece][square]
        elif piece.type is PieceType.PAWN:
            for sqr in attack_pawn_table[piece.player, square]:
                self.attack[piece][square].add(sqr)
                self.attacked_by[sqr][piece.player].add((piece.type, square))
            return
        for sqr in attack_table[piece.type, square]:
            self.attack[piece][square].add(sqr)
            self.attacked_by[sqr][piece.player].add((piece.type, square))

    def remove_slide_attack(self, square: Square) -> None:
        for player, attacked_by_sliding in self.attacked_by_sliding[square].items():
            for type, sqr, direction in attacked_by_sliding:
                piece = Piece((player, type))
                index = self.attack_sliding[piece][sqr][direction].index(square)
                remove_squares = self.attack_sliding[piece][sqr][direction][index + 1:]
                self.attack_sliding[piece][sqr][direction] = self.attack_sliding[piece][sqr][direction][:index + 1]
                self.attack[piece][sqr].difference_update(remove_squares)
                for s in remove_squares:
                    self.attacked_by_sliding[s][player].remove((type, sqr, direction))

    def add_slide_attack(self, square: Square) -> None:
        for player, attacked_by_sliding in self.attacked_by_sliding[square].items():
            for type, sqr, direction in attacked_by_sliding:
                piece = Piece((player, type))
                add_from = len(self.attack_sliding[piece][sqr][direction])
                add_squares = attack_sliding_table[type, sqr, direction][add_from:]
                for s in add_squares:
                    self.attack[piece][sqr].add(s)
                    self.attack_sliding[piece][sqr][direction].append(s)
                    self.attacked_by_sliding[s][player].add((type, sqr, direction))
                    if self.chessboard[s] is not Piece.NONE:
                        break
