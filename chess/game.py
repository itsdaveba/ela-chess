from .move import Move
from .position import Position


class ChessGame:
    def __init__(self) -> None:
        self.position = Position()
        self.outcome = ""
        self.status = "start"

    def reset(self):
        self.position.reset()
        self.outcome = ""
        self.status = "start"

    def play(self, fen: str = ""):
        if fen:
            self.position.fen = fen
        else:
            self.reset()
        self.status = "playing"

        while not self.outcome:
            print()
            print(self.position)
            print()
            move_str = input("Move: ").strip()

            try:
                move = Move(move_str.lower())
            except ValueError:
                if move_str.lower() == "undo":
                    try:
                        self.position.undo_move()
                    except ValueError:
                        print("\nNo previous moves")
                    continue
                elif move_str.lower() == "quit":
                    return
                print(f"\nInvalid move: '{move_str}'")
                continue

            if not self.position.make_move(move):
                print(f"\nIllegal move: '{move_str}'")
                continue

            in_check = self.position.in_check()

            if not self.position.has_legal_moves():
                if in_check:
                    print("\nCheckmate!")
                    if self.position.white:
                        self.outcome = "Black wins: 0-1"
                    else:
                        self.outcome = "White wins: 1-0"
                else:
                    print("\nStalemate!")
                    self.outcome = "Draw: 1/2-1/2"
                self.status = "finished"
            elif in_check:
                print("\nCheck!")

        print()
        print(self.position.board)
        print()
        print(self.outcome)
