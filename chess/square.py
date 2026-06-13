class Meta(type):
    def __iter__(cls):
        for value in range(8):
            yield cls(value)


class File(metaclass=Meta):
    def __init__(self, val: int | str) -> None:
        self.value: int
        self.char: str

        if isinstance(val, int):
            if not 0 <= val < 8:
                raise ValueError(f"invalid file value: {val}")

            self.value = val
            self.char = chr(ord('a') + self.value)
            return

        if len(val) != 1 or not 'a' <= val <= 'h':
            raise ValueError(f"invalid file char: {val}")

        self.value = ord(val) - ord('a')
        self.char = val

    def __repr__(self) -> str:
        return f"File.{self.char.upper()}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, File):
            return False
        return self.value == other.value


class Rank(metaclass=Meta):
    def __init__(self, val: int | str) -> None:
        self.value: int
        self.char: str

        if isinstance(val, int):
            if not 0 <= val < 8:
                raise ValueError(f"invalid rank value: {val}")

            self.value = val
            self.char = chr(ord('8') - self.value)
            return

        if len(val) != 1 or not '1' <= val <= '8':
            raise ValueError(f"invalid rank char: {val}")

        self.value = ord('8') - ord(val)
        self.char = val

    def __repr__(self) -> str:
        return f"Rank.{self.char.upper()}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rank):
            return False
        return self.value == other.value


class MetaSquare(type):
    def __iter__(cls):
        for rank in Rank:
            for file in File:
                yield cls(file, rank)


class Square(metaclass=MetaSquare):
    def __init__(self, *args) -> None:
        self.file: File
        self.rank: Rank
        self.str: str

        if len(args) == 1:
            square_str = args[0]
            if not isinstance(square_str, str):
                raise ValueError("invalid square arguments")
            if len(square_str) != 2:
                raise ValueError(f"invalid square string: {square_str}")
            file_char, rank_char = square_str
            self.file = File(file_char)
            self.rank = Rank(rank_char)
        elif len(args) == 2:
            file, rank = args
            if not isinstance(file, File) or not isinstance(rank, Rank):
                raise ValueError("invalid square arguments")
            self.file = file
            self.rank = rank
        else:
            raise ValueError("invalid square arguments")

        self.str = self.file.char + self.rank.char

    def __repr__(self) -> str:
        return f"Square.{self.str.upper()}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Square):
            return False
        return self.file == other.file and self.rank == other.rank
