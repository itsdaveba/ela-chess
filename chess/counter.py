

class Counter:
    def __init__(self, start: int | str) -> None:
        self.start: int
        self.value: int

        if isinstance(start, int):
            if start < 0:
                raise ValueError(f"invalid counter start: {start}")

            self.start = start
            self.value = start
            return

        if not start.isdigit():
            raise ValueError(f"invalid counter start: {start}")

        self.start = int(start)
        self.value = int(start)

    def __repr__(self) -> str:
        return f"Counter({self.value})"

    @property
    def str(self) -> str:
        return str(self.value)

    def next(self) -> None:
        self.value += 1

    def prev(self) -> None:
        self.value -= 1

    def reset(self) -> None:
        self.value = self.start
