order = "KQkq"
flag_value = {"K": 8, "Q": 4, "k": 2, "q": 1, "KQ": 12, "kq": 3}


class Castling:
    def __init__(self, val: int | str) -> None:
        self.rights: int

        if isinstance(val, int):
            if val < 0 or val >= 16:
                raise ValueError(f"invalid castling value: {val}")

            self.rights = val
            return

        if val == "-":
            self.rights = 0
            return

        n = len(val)
        if n <= 0 or n > 4:
            raise ValueError(f"invalid castling string: '{val}'")

        self.rights = i = j = 0
        while j != n:
            if i == 4:
                raise ValueError(f"invalid castling string: '{val}'")
            if order[i] == val[j]:
                self.rights += flag_value[val[j]]
                j += 1
            i += 1

    def __repr__(self) -> str:
        return f"Castling('{self.string}')"

    def __and__(self, other: str) -> int:
        return self.rights & flag_value[other]

    @property
    def string(self) -> str:
        string = [char for char in order if self.rights & flag_value[char]]

        if string:
            return "".join(string)
        return "-"

    def clear(self, flags: str) -> None:
        self.rights &= ~flag_value[flags]
