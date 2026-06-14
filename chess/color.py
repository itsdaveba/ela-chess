

class Color:
    def __init__(self, val: bool | str) -> None:
        self.white: bool
        self.char: str
        self.name: str

        if isinstance(val, bool):
            self.white = val
        else:
            if len(val) != 1 or val not in "wb":
                raise ValueError(f"invalid color char: {val}")
            self.white = val == 'w'

        self.char = "w" if self.white else "b"
        self.name = "WHITE" if self.white else "BLACK"

    def __repr__(self) -> str:
        return f"Color.{self.name}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Color):
            return False
        return self.white == other.white

    @property
    def opponent(self) -> "Color":
        return Color(not self.white)
