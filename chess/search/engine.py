import time
import random
from itertools import count

from ..evaluation.eval import evaluate

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
        self.nodes = 0
        self.max_nodes = max_nodes
        self.max_time = max_time if max_time <= 0 else time.perf_counter() + max_time / 1000

        ply = 0
        side = position.side

        moves = position.pseudo_legal_moves
        random.shuffle(moves)
        best_move = moves[0]

        iterator = count(1) if max_depth < 0 else range(1, max_depth + 1)

        for depth in iterator:
            max = MIN_VALUE
            random.shuffle(moves)
            bmove = moves[0]

            for move in moves:
                irrev = position.make_move(move)
                if not position.in_check(side):
                    try:
                        score = -self.negamax(position, depth - 1, ply + 1)
                    except TimeoutError:
                        return best_move
                    if score > max:
                        max = score
                        bmove = move
                position.undo_move(move, irrev)

            if max > 30000:
                return bmove
            if max < -30000:
                return bmove

            best_move = bmove

        return best_move

    def negamax(self, position: Position, depth: int, ply: int) -> int:
        self.nodes += 1

        if self.nodes % 500 == 0:
            if self.max_nodes >= 0 and self.nodes >= self.max_nodes:
                raise TimeoutError
            if self.max_time >= 0 and time.perf_counter() > self.max_time:
                raise TimeoutError

        if depth == 0:
            return evaluate(position)

        max = MIN_VALUE
        side = position.side
        moves = position.pseudo_legal_moves
        random.shuffle(moves)

        for move in moves:
            irrev = position.make_move(move)
            if not position.in_check(side):
                score = -self.negamax(position, depth - 1, ply + 1)
                if score > max:
                    max = score
            position.undo_move(move, irrev)

        if max == MIN_VALUE:
            return (max + ply) if position.in_check(side) else 0
        return max
