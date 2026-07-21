from time import sleep
from types import NoneType
from datetime import datetime

from .history import History
from .player import Player, HumanPlayer

from ..move.move import Move

from ..position.color import Color
from ..position.position import Position, SIDE_STRING

from ..search.engine import EnginePlayer


STARTING_POSITION_FEN: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
EVENT: dict[tuple[type, type], str] = {
    (HumanPlayer, HumanPlayer): "Player Match",
    (HumanPlayer, EnginePlayer): "Player vs Engine",
    (EnginePlayer, HumanPlayer): "Player vs Engine",
    (EnginePlayer, EnginePlayer): "Engine Match"
}
PLAYER_NAME: dict[type, str] = {
    HumanPlayer: "Player",
    EnginePlayer: "ElaChess",
    NoneType: "?"
}
RESULT: list[str] = ["1-0", "0-1", "1/2-1/2"]


class ChessGame:
    def __init__(self, fen: str | None = None) -> None:
        self.fen: str
        self.playing: bool
        self.winner: Color
        self.history: History
        self.position: Position
        self.white: Player | None
        self.black: Player | None

        self.reset(fen)

    def __repr__(self) -> str:
        string = "ChessGame("
        if self.fen != STARTING_POSITION_FEN:
            string += f"fen='{self.fen}', "
        string += f"white={self.white}, "
        string += f"black={self.black}, "
        result = None if self.playing else self.winner
        string += f"result={result!s}, "
        return string + f"history={self.history.moves})"

    def __str__(self) -> str:
        return self.pgn

    @property
    def pgn(self) -> str:
        try:
            pgn = [f'[Event "{EVENT[(type(self.white), type(self.black))]}"]']
        except KeyError:
            pgn = ['[Event "?"]']
        pgn.append('[Site "Ela Chess"]')
        pgn.append(f'[Date "{datetime.today().strftime("%Y.%m.%d")}"]')
        pgn.append('[Round "?"]')
        pgn.append(f'[White "{PLAYER_NAME[type(self.white)]}"]')
        pgn.append(f'[Black "{PLAYER_NAME[type(self.black)]}"]')
        result = "*" if self.playing else RESULT[self.winner]
        pgn.append(f'[Result "{result}"]')
        if self.fen != STARTING_POSITION_FEN:
            pgn.append('[SetUp "1"]')
            pgn.append(f'[FEN "{self.fen}"]')

        pgn.append('')
        pgn.append(self.history.movetext())

        return "\n".join(pgn)

    def save_pgn(self, filename: str | None = None) -> None:
        if filename is None:
            white = PLAYER_NAME[type(self.white)]
            white = "_" if white == "?" else white
            black = PLAYER_NAME[type(self.black)]
            black = "_" if black == "?" else black
            filename = f"{white}_vs_{black}_{datetime.today().strftime('%Y.%m.%d')}.pgn"

        with open(filename, "w") as file:
            file.write(self.pgn)

        print(f"PGN file saved: '{filename}'")

    def reset(self, fen: str | None = None) -> None:
        self.fen = STARTING_POSITION_FEN if fen is None else fen
        self.playing = True
        self.winner = Color.NONE
        self.history = History()
        self.position = Position(self.fen)
        self.white = None
        self.black = None

    def display(self) -> None:
        print(self.position)

    def make_move(self, move: Move | str) -> bool:
        if isinstance(move, str):
            parsed = self._parse_move(move)

            if parsed is None:
                return False

            move = parsed

        side = self.position.side
        irrev = self.position.make_move(move)

        if self.position.in_check(side):
            print(f"Illegal move: '{move}'")
            self.position.undo_move(move, irrev)
            return False

        self.history.append(move, irrev)

        return True

    def undo_move(self) -> Move | None:
        try:
            move, irrev = self.history.pop()
        except IndexError:
            print("No previous move")
            return None

        self.playing = True
        self.winner = Color.NONE
        self.position.undo_move(move, irrev)

        return move

    def has_legal_moves(self) -> bool:
        side = self.position.side

        for move in self.position.pseudo_legal_moves:
            irrev = self.position.make_move(move)

            if not self.position.in_check(side):
                self.position.undo_move(move, irrev)
                return True
            self.position.undo_move(move, irrev)

        return False

    def play(self, white: Player, black: Player, time: int, depth: int, nodes: int) -> None:
        self.white = white
        self.black = black

        print(f"\n{EVENT[(type(self.white), type(self.black))]}\n")
        print(f"White: {white}")
        print(f"Black: {black}")
        print(f"\n{self.position}\n")

        if self.has_legal_moves() and self.position.halfmove.value < 100:
            self.playing = True
            self.winner = Color.NONE
        else:
            self.playing = False
            self.winner = self._get_winner()

        while self.playing:
            player = white if self.position.side == Color.WHITE else black
            move = player.search(self.position.copy(), time, depth, nodes)

            if isinstance(move, str):
                if move in ("exit", "quit", "resign"):
                    self.playing = False
                    self.winner = self.position.side.opponent
                    print(f"\n{SIDE_STRING[self.position.side]} resigns")
                    break

                if move == "undo":
                    if len(self.history) < 2:
                        print("No previous move")
                    else:
                        self.undo_move()
                        self.undo_move()
                        print(f"\n{self.position}\n")
                    continue

            else:
                print(f"Engine move: {move}")

            if self.make_move(move):
                print(f"\n{self.position}\n")

                if not self.has_legal_moves():
                    self.playing = False
                    self.winner = self._get_winner()

                elif self.position.halfmove.value >= 100:
                    print("Fifty-move rule")
                    self.playing = False
                    self.winner = Color.NONE

            sleep(0.1)

        print(f"\nResult: {RESULT[self.winner]}")
        print("Draw\n" if self.winner == Color.NONE else f"{SIDE_STRING[self.winner]} wins\n")

    def _get_winner(self) -> Color:
        if self.position.in_check(self.position.side):
            print("Checkmate")
            return self.position.side.opponent
        else:
            print("Stalemate")
            return Color.NONE

    def _parse_move(self, move_str: str) -> Move | None:
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
