class Counter:
    def __init__(self, value: int) -> None:
        self.value: int = value

    def __repr__(self) -> str:
        return f"Counter({self.value})"

    @classmethod
    def from_string(cls, string: str) -> "Counter":
        if string.isdigit():
            return Counter(int(string))
        raise ValueError(f"invalid counter string '{string}'")

    @property
    def string(self) -> str:
        return str(self.value)
