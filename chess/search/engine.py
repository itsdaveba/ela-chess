import sys
import time
import random

from ..evaluation.eval import evaluate

from ..game.player import Player

from ..move.move import Move

from ..position.position import Position


MAX_DEPTH: int = 128
TIME_CONTROL_FREQ: int = 500

MIN_SCORE: int = -50000
MATE_CUTOFF: int = 30000


class EnginePlayer(Player):
    name = "Engine"

    def __init__(self) -> None:
        super().__init__()
        self.nodes: int
        self.stop: bool
        self.max_nodes: int
        self.max_time: float
        self.best_move: Move
        self.pv: list[list[Move]]

    def print_uci_info(self, depth: int, score_type: str, score: int, current_time: float, pv: list[Move]) -> None:
        score_key = f"score {score_type}"

        info = {
            "depth": depth,
            score_key: score,
            "nodes": self.nodes,
            "nps": int(self.nodes / current_time),
            "time": int(current_time * 1000)
        }

        sys.stdout.write("info ")
        for key in ["depth", score_key, "nodes", "nps", "time"]:
            sys.stdout.write(f"{key} {info[key]} ")
        sys.stdout.write(f"pv {' '.join(map(str, pv))}\n")
        sys.stdout.flush()

    def search(self, position: Position, max_time: int, max_depth: int,
               max_nodes: int, print_uci_info: bool = False) -> Move | str:
        self.nodes = 0
        self.stop = False
        self.max_nodes = max_nodes

        start_time = time.perf_counter()
        self.max_time = max_time if max_time <= 0 else start_time + max_time / 1000

        moves = position.pseudo_legal_moves
        self.best_move = moves[0]

        if max_depth < 0:
            max_depth = MAX_DEPTH
        self.pv = [[moves[0]] * depth for depth in range(max_depth, -1, -1)]

        side = position.side

        for depth in range(1, max_depth + 1):
            alpha = MIN_SCORE
            random.shuffle(moves)

            for move in moves:
                irrev = position.make_move(move)
                if not position.in_check(side):
                    try:
                        score = -self.negamax(position, MIN_SCORE, -alpha, depth - 1, 1)
                    except TimeoutError:
                        return self.best_move
                    if score > alpha:
                        alpha = score
                        self.pv[0][0] = move
                        self.pv[0][1:depth] = self.pv[1][:depth - 1]
                position.undo_move(move, irrev)

            self.best_move = self.pv[0][0]
            current_time = time.perf_counter() - start_time

            if abs(alpha) > MATE_CUTOFF:
                if print_uci_info:
                    score = depth // 2 if alpha > 0 else -(depth // 2)
                    self.print_uci_info(depth, "mate", score, current_time, self.pv[0][:depth - 1])
                return self.best_move

            if print_uci_info:
                self.print_uci_info(depth, "cp", alpha, current_time, self.pv[0][:depth])

        return self.best_move

    def negamax(self, position: Position, alpha: int, beta: int, depth: int, ply: int) -> int:
        self.nodes += 1

        if self.nodes % TIME_CONTROL_FREQ == 0:
            if self.stop:
                raise TimeoutError
            if self.max_nodes >= 0 and self.nodes >= self.max_nodes:
                raise TimeoutError
            if self.max_time >= 0 and time.perf_counter() > self.max_time:
                raise TimeoutError

        if depth == 0:
            return evaluate(position)

        side = position.side
        no_legal_moves = True
        moves = position.pseudo_legal_moves
        random.shuffle(moves)

        for move in moves:
            irrev = position.make_move(move)
            if not position.in_check(side):
                no_legal_moves = False
                score = -self.negamax(position, -beta, -alpha, depth - 1, ply + 1)
                if score >= beta:
                    position.undo_move(move, irrev)
                    return beta
                if score > alpha:
                    alpha = score
                    self.pv[ply][0] = move
                    self.pv[ply][1:depth] = self.pv[ply+1][:depth - 1]
            position.undo_move(move, irrev)

        if no_legal_moves:
            return (MIN_SCORE + ply) if position.in_check(side) else 0
        return alpha
