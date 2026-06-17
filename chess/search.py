import sys
import random

from .move import Move
from .position import Position


class Player:
    def __init__(self, uci: bool = False) -> None:
        self.uci: bool = uci

    def search(self, position: Position, depth: int = -1) -> Move | None:
        raise NotImplementedError  # pragma: no cover

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(uci={self.uci})"


class Human(Player):
    def search(self, position: Position, depth: int = -1) -> Move | None:
        while True:
            print()
            print(position)
            print()
            move_str = input("Move: ").strip()

            try:
                move = Move(move_str.lower())
            except ValueError:
                if move_str.lower() == "undo":
                    try:
                        position.undo_move()
                        position.undo_move()
                    except ValueError:
                        print("\nNo previous moves")
                    continue
                elif move_str.lower() == "resign":
                    return None
                print(f"\nInvalid move: '{move_str}'")
                continue

            if position.is_legal_move(move):
                return move
            print(f"\nIllegal move: '{move_str}'")


class Engine(Player):
    def search(self, position: Position, depth: int = -1) -> Move | None:

        move = random.choice(position.pseudo_legal_moves)
        while not position.is_legal_move(move):
            move = random.choice(position.pseudo_legal_moves)  # pragma: no cover

        if self.uci:
            sys.stdout.write(f"bestmove {move}\n")
            sys.stdout.flush()
        else:
            print(f"\nEngine move: {move}")

        return move
