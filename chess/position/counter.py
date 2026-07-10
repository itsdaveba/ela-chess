class Counter:
    def __init__(self, value: int) -> None:
        self.value: int
        self.reset(value)

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

    def copy(self) -> "Counter":
        return Counter(self.value)

    def incr(self) -> None:
        self.value += 1

    def decr(self) -> None:
        self.value -= 1

    def reset(self, value: int = 0):
        self.value = value
