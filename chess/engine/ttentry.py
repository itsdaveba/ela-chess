from enum import Enum
from dataclasses import dataclass

from ..move.move import Move


ENTRY_BYTE_SIZE = 386


class NodeType(int, Enum):
    PVNode = 0
    AllNode = 1
    CutNode = 2

    NONE = 3


@dataclass
class TTEntry:
    hash: int
    best: Move
    depth: int
    score: int
    type: NodeType

    @classmethod
    def null(cls) -> "TTEntry":
        return cls(0, Move.none(), 0, 0, NodeType.NONE)
