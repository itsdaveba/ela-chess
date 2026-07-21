from abc import ABC, abstractmethod

from ..move.move import Move

from ..position.position import Position


class Player(ABC):
    name: str

    def __repr__(self) -> str:
        return self.name

    @abstractmethod
    def search(self, position: Position, max_time: int, max_depth: int,
               max_nodes: int, print_uci_info: bool = False) -> Move | str:
        ...


class HumanPlayer(Player):
    name = "Human"

    def search(self, position: Position, max_time: int, max_depth: int,
               max_nodes: int, print_uci_info: bool = False) -> Move | str:
        return input("Move: ")
