import random

from ..game.player import Player

from ..move.move import Move

from ..position.position import Position


MIN_VALUE: int = -50000


class EnginePlayer(Player):
    name = "Engine"

    def __init__(self) -> None:
        super().__init__()
        self.nodes: int
        self.max_nodes: int
        self.max_time: float

    def best_move(self, position: Position, max_time: int, max_depth: int, max_nodes: int) -> Move | str:
        side = position.side
        moves = position.pseudo_legal_moves
        random.shuffle(moves)

        for move in moves:
            irrev = position.make_move(move)
            if not position.in_check(side):
                return move
            position.undo_move(move, irrev)

        return "resign"  # pragma: no cover
