import random

from ..evaluation.eval import evaluate

from ..game.player import Player

from ..move.move import Move

from ..position.position import Position


MIN_VALUE: int = -50000


class EnginePlayer(Player):
    name = "Engine"

    def best_move(self, position: Position, max_time: int, max_depth: int, max_nodes: int) -> Move | str:
        side = position.side
        moves = position.pseudo_legal_moves
        random.shuffle(moves)
        best_move = "resign"

        if max_depth == 0:
            for move in moves:
                irrev = position.make_move(move)
                if not position.in_check(side):
                    position.undo_move(move, irrev)
                    return move
                position.undo_move(move, irrev)

        max = -float("inf")
        for move in moves:
            irrev = position.make_move(move)
            if not position.in_check(side):
                score = -self.negamax(position, max_depth - 1)
                if score > max:
                    max = score
                    best_move = move
            position.undo_move(move, irrev)

        return best_move

    def negamax(self, position: Position, depth: int) -> int:
        if depth == 0:
            return evaluate(position)

        max = MIN_VALUE
        side = position.side
        for move in position.pseudo_legal_moves:
            irrev = position.make_move(move)
            if not position.in_check(side):
                score = -self.negamax(position, depth - 1)
                if score > max:
                    max = score
            position.undo_move(move, irrev)

        if max == MIN_VALUE and not position.in_check(side):
            return 0
        return max
