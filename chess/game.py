from .search import Player, Human, Engine
from .position import Position, INITIAL_FEN


player_name = ["Black", "White"]
result = ["0-1", "1-0"]
player_map: dict[str, type[Player]] = {"human": Human, "engine": Engine}


class ChessGame:
    def __init__(self) -> None:
        self.position: Position = Position()

    def play(self, fen: str | None, wplayer: str, bplayer: str) -> str:
        if fen is None:
            fen = INITIAL_FEN
        self.position.fen = fen

        outcome = ""
        white_player = player_map[wplayer]()
        black_player = player_map[bplayer]()

        print("\nEnter a move, 'undo', or 'resign'")

        while True:
            move = white_player.search(self.position) if self.position.white else black_player.search(self.position)

            if move is None:
                outcome = f"{player_name[self.position.white]} resigns: {result[not self.position.white]}"
                break

            self.position.make_move(move)

            in_check = self.position.in_check()

            if not self.position.has_legal_moves():
                if in_check:
                    print("\nCheckmate!")
                    outcome = f"{player_name[not self.position.white]} wins: {result[not self.position.white]}"
                    break
                print("\nStalemate!")
                outcome = "Draw: 1/2-1/2"
                break

            if self.position.halfmove == 100:
                print("\nDraw by 50-move rule")
                outcome = "Draw: 1/2-1/2"
                break

            if in_check:
                print("\nCheck!")

        print()
        print(outcome)
        print(self.position.board)

        return outcome
