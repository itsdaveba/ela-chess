import sys
import time
import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game.game import ChessGame

from .ttentry import TTEntry, NodeType, ENTRY_BYTE_SIZE

from ..game.player import Player

from ..move.move import Move, MoveType

from ..position.position import Color


MAX_DEPTH: int = 128
TIME_CONTROL_FREQ: int = 1000

MIN_SCORE: int = -50000
MATE_CUTOFF: int = 30000

# MB
MIN_HASH_SIZE: int = 1
MAX_HASH_SIZE: int = 8192
DEFAULT_HASH_SIZE: int = 512

ENTRIES_PER_MB = (1024 * 1024) // ENTRY_BYTE_SIZE


class EnginePlayer(Player):
    name = "Engine"

    def __init__(self) -> None:
        super().__init__()

        self.tt: list[TTEntry]
        self.num_entries: int
        self._hash_size: int

        self.nodes: int
        self.stop: bool
        self.max_nodes: int
        self.max_time: float
        self.best_move: Move

        self.hash_size = DEFAULT_HASH_SIZE

    @property
    def hash_size(self) -> int:
        return self._hash_size

    @hash_size.setter
    def hash_size(self, hash_size: int) -> None:
        self._hash_size = hash_size
        self.num_entries = ENTRIES_PER_MB * hash_size
        self.reset()

    def reset(self) -> None:
        self.tt = [TTEntry.null()] * self.num_entries

    def print_info(self, depth: int, score_type: str, score: int, time_elapsed: float, pv: list[Move]) -> None:
        score_key = f"score {score_type}"

        info = {
            "depth": depth,
            score_key: score,
            "nodes": self.nodes,
            "nps": int(self.nodes / time_elapsed),
            "time": int(time_elapsed * 1000),
            "pv": " ".join(map(str, pv))
        }

        sys.stdout.write("info")
        for key in ["depth", score_key, "nodes", "nps", "time", "pv"]:
            sys.stdout.write(f" {key} {info[key]}")
        sys.stdout.write("\n")
        sys.stdout.flush()

    def pv(self, game: "ChessGame", best_move: Move) -> list[Move]:
        pv = [best_move]
        game.make_move(best_move)

        if not game.repetition() and game.halfmove.value < 100:
            ttentry = self.tt[game.hash % self.num_entries]
            if ttentry.hash == game.hash and ttentry.type == NodeType.PVNode:
                pv.extend(self.pv(game, ttentry.best))

        game.undo_move()
        return pv

    def search(self, game: "ChessGame", max_time: int, max_depth: int,
               max_nodes: int, print_info: bool = False) -> Move | str:
        self.nodes = 0
        self.stop = False
        self.max_nodes = max_nodes

        start_time = time.perf_counter()
        self.max_time = max_time if max_time <= 0 else start_time + max_time / 1000
        self.best_move = Move.none()

        game = game.copy()
        moves = game.pseudo_legal_moves
        random.shuffle(moves)

        for move in moves:
            if game.make_move(move):
                self.best_move = move
                game.undo_move()
                break

        if self.best_move.type == MoveType.NONE:
            if print_info:
                sys.stdout.write(f"info depth 0 score {'mate' if game.in_check() else 'cp'} 0\n")
                sys.stdout.flush()
            return self.best_move

        key = game.hash % self.num_entries
        ttentry = self.tt[key]

        for depth in range(1, (MAX_DEPTH if max_depth < 0 else max_depth) + 1):

            alpha = MIN_SCORE
            random.shuffle(moves)
            best_move = Move.none()

            if ttentry.hash == game.hash and ttentry.depth:
                moves.insert(0, moves.pop(moves.index(ttentry.best)))

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

            if ttentry.depth <= depth:
                self.tt[key] = TTEntry(game.hash, best_move, depth, alpha, NodeType.PVNode)

            self.best_move = best_move
            time_elapsed = time.perf_counter() - start_time

            if abs(alpha) > MATE_CUTOFF:
                if print_info:
                    score = depth // 2 if alpha > 0 else -(depth // 2)
                    self.print_info(depth, "mate", score, time_elapsed, self.pv(game, best_move))
                return self.best_move

            if print_info:
                self.print_info(depth, "cp", alpha, time_elapsed, self.pv(game, best_move))

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

        if game.repetition(2) or game.halfmove.value >= 100:
            return 0

        if depth == 0:
            return game.eval if game.side == Color.WHITE else -game.eval

        moves = game.pseudo_legal_moves

        type = NodeType.AllNode
        best_score = MIN_SCORE
        random.shuffle(moves)
        best_move = Move.none()

        key = game.hash % self.num_entries
        ttentry = self.tt[key]

        if ttentry.hash == game.hash and ttentry.depth:
            moves.insert(0, moves.pop(moves.index(ttentry.best)))

        for move in moves:
            if game.make_move(move):
                score = -self.negamax(game, -beta, -alpha, depth - 1, ply + 1)
                game.undo_move()
                if score >= beta:
                    best_move = move
                    best_score = score
                    type = NodeType.CutNode
                    break
                if score > alpha:
                    alpha = score
                    type = NodeType.PVNode
                if score > best_score:
                    best_move = move
                    best_score = score

        if best_move.type == MoveType.NONE:
            return (MIN_SCORE + ply) if game.in_check() else 0

        if ttentry.depth < depth or (ttentry.depth == depth and ttentry.type != NodeType.PVNode):
            self.tt[key] = TTEntry(game.hash, best_move, depth, best_score, type)

        return best_score
