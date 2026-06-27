class Counter:
    @classmethod
    def from_string(cls, string: str) -> "Counter":
        return Counter()

    @property
    def string(self) -> str:
        return ""
