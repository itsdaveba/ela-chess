import sys
import time
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game.game import ChessGame

from ..game.player import Player

from ..move.move import Move, MoveType

from ..position.position import Color


MAX_DEPTH: int = 128
TIME_CONTROL_FREQ: int = 1000

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

    def print_uci_info(self, depth: int, score_type: str, score: int, time_elapsed: float, pv: list[Move]) -> None:
        score_key = f"score {score_type}"

        info = {
            "depth": depth,
            score_key: score,
            "nodes": self.nodes,
            "nps": int(self.nodes / time_elapsed),
            "time": int(time_elapsed * 1000)
        }

        sys.stdout.write("info ")
        for key in ["depth", score_key, "nodes", "nps", "time"]:
            sys.stdout.write(f"{key} {info[key]} ")
        sys.stdout.write(f"pv {' '.join(map(str, pv))}\n")
        sys.stdout.flush()

    def search(self, game: "ChessGame", max_time: int, max_depth: int,
               max_nodes: int, print_uci_info: bool = False) -> Move | str:
        self.nodes = 0
        self.stop = False
        self.max_nodes = max_nodes

        start_time = time.perf_counter()
        self.max_time = max_time if max_time <= 0 else start_time + max_time / 1000
        self.best_move = Move.none()

        moves = game.pseudo_legal_moves
        random.shuffle(moves)

        for move in moves:
            if game.make_move(move):
                self.best_move = move
                game.undo_move()
                break

        if self.best_move.type == MoveType.NONE:
            if print_uci_info:
                sys.stdout.write(f"info depth 0 score {'mate' if game.in_check() else 'cp'} 0\n")
                sys.stdout.flush()
            return self.best_move

        for depth in range(1, (MAX_DEPTH if max_depth < 0 else max_depth) + 1):

        for depth in range(1, max_depth + 1):
            alpha = MIN_SCORE
            random.shuffle(moves)
            best_move = Move.none()

            for move in moves:
                if game.make_move(move):
                    try:
                        score = -self.negamax(game, MIN_SCORE, -alpha, depth - 1, 1)
                    except TimeoutError:
                        return self.best_move
                    game.undo_move()
                    if score > alpha:
                        alpha = score
                        best_move = move

            self.best_move = best_move
            time_elapsed = time.perf_counter() - start_time

            if abs(alpha) > MATE_CUTOFF:
                if print_uci_info:
                    score = depth // 2 if alpha > 0 else -(depth // 2)
                    self.print_uci_info(depth, "mate", score, time_elapsed, [best_move])
                return self.best_move

            if print_uci_info:
                self.print_uci_info(depth, "cp", alpha, time_elapsed, [best_move])

        return self.best_move

    def negamax(self, game: "ChessGame", alpha: int, beta: int, depth: int, ply: int) -> int:
        self.nodes += 1

        if self.nodes % TIME_CONTROL_FREQ == 0:
            if self.stop:
                raise TimeoutError
            if self.max_nodes >= 0 and self.nodes >= self.max_nodes:
                raise TimeoutError
            if self.max_time >= 0 and time.perf_counter() > self.max_time:
                raise TimeoutError

        if game.repetition() or game.halfmove.value >= 100:
            return 0

        if depth == 0:
            return game.eval if game.side == Color.WHITE else -game.eval

        moves = game.pseudo_legal_moves

        best_score = MIN_SCORE
        random.shuffle(moves)
        best_move = Move.none()

        for move in moves:
            if game.make_move(move):
                score = -self.negamax(game, -beta, -alpha, depth - 1, ply + 1)
                game.undo_move()
                if score >= beta:
                    return score
                if score > alpha:
                    alpha = score
                if score > best_score:
                    best_move = move
                    best_score = score

        if best_move.type == MoveType.NONE:
            return (MIN_SCORE + ply) if game.in_check() else 0
        return best_score
