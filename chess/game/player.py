import random
from abc import ABC, abstractmethod

from ..move.move import Move

from ..position.position import Position


class Player(ABC):
    name: str

    def __repr__(self) -> str:
        return self.name

    @abstractmethod
    def best_move(self, position: Position) -> Move | str:
        ...


class HumanPlayer(Player):
    name = "Human"

    def best_move(self, position: Position) -> Move | str:
        return input("Move: ")


class EnginePlayer(Player):
    name = "Engine"

    def best_move(self, position: Position) -> Move | str:
        side = position.side
        moves = position.pseudo_legal_moves
        random.shuffle(moves)

        for move in moves:
            irrev = position.make_move(move)
            if not position.in_check(side):
                position.undo_move(move, irrev)
                return move
            position.undo_move(move, irrev)  # pragma: no cover

        return "resign"  # pragma: no cover
