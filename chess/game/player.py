from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

if TYPE_CHECKING:
    from ..game.game import ChessGame

from ..move.move import Move


class Player(ABC):
    name: str

    def __repr__(self) -> str:
        return self.name

    @abstractmethod
    def search(self, game: "ChessGame", max_time: int, max_depth: int,
               max_nodes: int, print_uci_info: bool = False) -> Move | str:
        ...


class HumanPlayer(Player):
    name = "Human"

    def search(self, game: "ChessGame", max_time: int, max_depth: int,
               max_nodes: int, print_uci_info: bool = False) -> Move | str:
        return input("Move: ")
