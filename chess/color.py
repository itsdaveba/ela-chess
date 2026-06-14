

class Color:
    def __init__(self, val: bool | str) -> None:
        self.white: bool

        if isinstance(val, bool):
            self.white = val
            return

        if len(val) != 1 or val not in "wb":
            raise ValueError(f"invalid color char: {val}")

        self.white = val == 'w'

    def __repr__(self) -> str:
        return f"Color.{self.name}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Color):
            return False
        return self.white == other.white

    @property
    def char(self) -> str:
        return "w" if self.white else "b"

    @property
    def name(self) -> str:
        return "WHITE" if self.white else "BLACK"

    @property
    def opponent(self) -> "Color":
        return Color(not self.white)
