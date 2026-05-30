from collections import defaultdict

from defs import Piece, PieceType, Player, Direction, Square, Move


piece_movement: dict[PieceType, list[Direction]] = {
    # The bishop may move to any square along a diagonal on which it stands.
    PieceType.BISHOP: [Direction.UP_RIGHT, Direction.UP_LEFT, Direction.DOWN_LEFT, Direction.DOWN_RIGHT],
    # The rook may move to any square along the file or the rank on which it stands.
    PieceType.ROOK: [Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.DOWN],
    # The queen may move to any square along the file, the rank or a diagonal on which it stands.
    PieceType.QUEEN: [Direction.UP_RIGHT, Direction.UP_LEFT, Direction.DOWN_LEFT, Direction.DOWN_RIGHT,
                      Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.DOWN]
}


class Board:
    def __init__(self) -> None:
        # The chessboard is composed of an 8 x 8 grid of 64 equal squares.
        # The initial position of the pieces on the chessboard is as follows:
        self.chessboard: list[list[Piece]] = [
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
        # The player with the white pieces commences the game.
        self.player: Player = Player.WHITE

        self.piece_square: dict[Player, dict[PieceType, set[Square]]] = {Player.WHITE: defaultdict(set),
                                                                         Player.BLACK: defaultdict(set)}
        for r, rank in enumerate(self.chessboard):
            for f, piece in enumerate(rank):
                if piece is Piece.NONE:
                    continue
                self.piece_square[piece.player][piece.type].add(Square(r, f))

        assert len(self.piece_square[Player.WHITE][PieceType.KING]) == 1
        assert len(self.piece_square[Player.BLACK][PieceType.KING]) == 1

    def __str__(self) -> str:
        return "\n".join([" ".join([piece.chr for piece in rank]) for rank in self.chessboard])

    def __getitem__(self, key: Square) -> Piece:
        return self.chessboard[key.rank][key.file]

    def __setitem__(self, key: Square, value: Piece) -> None:
        self.chessboard[key.rank][key.file] = value

    def make_move(self, move: Move) -> bool:
        # who move their pieces alternately on a square board called a ‘chessboard’.
        src_piece = self[move.src]
        dst_piece = self[move.dst]
        if src_piece.player is not self.player:
            print(f"Player {self.player} needs to move its own piece")
            return False
        if move.src == move.dst:
            print("Not permitted to move to same square")
            return False

        if src_piece.type in (PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN):
            if move.dst not in self.squares_attacked_by_piece_type_at_square(src_piece.type, move.src):
                print(f"{move.dst} not reachable by {src_piece} at {move.src}")
                return False

        # It is not permitted to move a piece to a square occupied by a piece of the same colour.
        if dst_piece.player is self.player:
            print("Not permitted to move to same color")
            return False
        # and also ’capturing’ the opponent’s king are not allowed.
        if dst_piece.type is PieceType.KING:
            print("Cannot capture opponent's king")
            return False

        king_under_attack = self.player_king_under_attack()
        # If a piece moves to a square occupied by an opponent’s piece
        # the latter is captured and removed from the chessboard as part of the same move.
        self[move.dst] = src_piece
        self[move.src] = Piece.NONE
        if dst_piece is not Piece.NONE:
            self.piece_square[dst_piece.player][dst_piece.type].remove(move.dst)
        self.piece_square[src_piece.player][src_piece.type].add(move.dst)
        self.piece_square[src_piece.player][src_piece.type].remove(move.src)
        if self.player_king_under_attack():
            # Leaving one’s own king under attack
            if king_under_attack:
                print("Cannot leave own king under attack")
            # exposing one’s own king to attack
            else:
                print("Cannot expose own king to attack")
            self[move.src] = src_piece
            self[move.dst] = dst_piece
            self.piece_square[src_piece.player][src_piece.type].add(move.src)
            self.piece_square[src_piece.player][src_piece.type].remove(move.dst)
            if dst_piece is not Piece.NONE:
                self.piece_square[dst_piece.player][dst_piece.type].add(move.dst)
            return False

        self.player = self.player.opponent
        return True

    # The objective of each player is to place the opponent’s king ‘under attack’
    def player_king_under_attack(self) -> bool:
        king_square = next(iter(self.piece_square[self.player][PieceType.KING]))
        return king_square in self.squares_attacked_by_player(self.player.opponent)

    def squares_attacked_by_player(self, player: Player) -> set[Square]:
        attacked_squares = set()
        for piece_type, squares in self.piece_square[player].items():
            for square in squares:
                attacked_squares.update(self.squares_attacked_by_piece_type_at_square(piece_type, square))
        return attacked_squares

    # in such a way that the opponent has no legal move.
    def no_legal_move(self) -> bool:
        # seylf.player no legal moves
        return False

    # If the position is such that neither player can possibly checkmate, the game is drawn.
    def no_possible_checkmate(self) -> bool:
        return False

    # A piece is said to attack an opponent’s piece if the piece could make a capture on that square
    # according to the Articles 3.2 to 3.8.
    def is_piece_attacked_by_opponent_piece(self, piece: Piece, opponent_piece: Piece) -> bool:
        return False

    # A piece is considered to attack a square, even if such a piece is constrained from moving to that square
    # because it would then leave or place the king of its own colour under attack.
    def is_square_attacked_by_piece(self, square: Square, piece: Piece) -> bool:
        return False

    # TODO keep this in memory?
    def squares_attacked_by_piece_type_at_square(self, piece_type: PieceType, square: Square) -> set[Square]:
        squares_attacked = set()
        if piece_type in (PieceType.BISHOP, PieceType.ROOK, PieceType.QUEEN):
            for direction in piece_movement[piece_type]:
                new_square = square + direction
                while new_square.is_valid():
                    squares_attacked.add(new_square)
                    if self[new_square] is not Piece.NONE:
                        break
                    new_square += direction
        return squares_attacked
