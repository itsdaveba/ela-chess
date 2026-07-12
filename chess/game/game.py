import time

from .player import Player
from .history import History

from ..move.move import Move

from ..position.color import Color
from ..position.position import Position, SIDE_STRING


STARTING_POSITION_FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
RESULT: list[str] = ["1-0", "0-1", "1/2-1/2"]


class ChessGame:
    def __init__(self, white: Player, black: Player, fen: str | None = None) -> None:
        self.white: Player = white
        self.black: Player = black

        self.fen: str
        self.position: Position
        self.history: History

        self.reset(fen)

    def __repr__(self) -> str:
        string = f"ChessGame(white='{self.white.name.lower()}', black='{self.black.name.lower()}', "
        if self.fen != STARTING_POSITION_FEN:
            string += f"fen='{self.fen}', "
        return string + f"history={self.history.moves})"

    def reset(self, fen: str | None = None) -> None:
        self.fen = STARTING_POSITION_FEN if fen is None else fen
        self.position = Position(self.fen)
        self.history = History()

    def make_move(self, move: Move) -> bool:
        side = self.position.side

        irrev = self.position.make_move(move)

        if self.position.in_check(side):
            self.position.undo_move(move, irrev)
            return False

        self.history.append(move, irrev)

        return True

    def undo_move(self) -> None:
        try:
            move, irrev = self.history.pop()
        except IndexError:
            raise ValueError("no previous move")

        self.position.undo_move(move, irrev)

    def has_legal_moves(self) -> bool:
        side = self.position.side

        for move in self.position.pseudo_legal_moves:
            irrev = self.position.make_move(move)

            if not self.position.in_check(side):
                self.position.undo_move(move, irrev)
                return True
            self.position.undo_move(move, irrev)

        return False

    def play(self) -> None:
        playing: bool
        winner: Color

        print("\nChess Game\n")
        print(f"White: {self.white}")
        print(f"Black: {self.black}")
        print(f"\n{self.position}\n")

        if self.has_legal_moves():
            playing = True
            winner = Color.NONE
        else:
            playing = False
            winner = self._get_winner()

        while playing:
            player = self.white if self.position.side == Color.WHITE else self.black
            move = player.best_move(self.position)

            if isinstance(move, str):
                if move in ("exit", "quit", "resign"):
                    print(f"\n{SIDE_STRING[self.position.side]} resigns")
                    playing = False
                    winner = self.position.side.opponent
                    break

                move = self._parse_move(move)
                if move is None:
                    continue

            else:
                print(f"Engine move: {move}")

            if self.make_move(move):
                print(f"\n{self.position}\n")

                if not self.has_legal_moves():
                    playing = False
                    winner = self._get_winner()
            else:
                print(f"Illegal move: '{move}'")

            time.sleep(0.1)

        print(f"\nResult: {RESULT[winner]}")
        if winner == Color.NONE:
            print("Draw\n")
        else:
            print(f"{SIDE_STRING[winner]} wins\n")

    def _get_winner(self) -> Color:
        if self.position.in_check(self.position.side):
            print("Checkmate")
            return self.position.side.opponent
        else:
            print("Stalemate")
            return Color.NONE

    def _parse_move(self, move_str: str) -> Move | None:
        if move_str == "undo":
            if len(self.history) < 2:
                print("No previous move")
            else:
                self.undo_move()
                self.undo_move()
                print(f"\n{self.position}\n")
            return None

        try:
            move = Move.from_string(move_str)
        except ValueError:
            print(f"Invalid move: '{move_str}'")
            return None

        try:
            moves = self.position.pseudo_legal_moves
            return moves[moves.index(move)]
        except ValueError:
            print(f"Illegal move: '{move}'")
            return None
