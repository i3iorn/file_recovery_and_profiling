from src.string import EnhancedString


class EnhancedLine:
    def __init__(self, line: bytes, delimiter: bytes, encoding: str):
        self.__line = line.replace(b"'", b"").replace(b'"', b'')
        self.__delimiter = delimiter
        self.__encoding = encoding

    def __repr__(self):
        return f"EnhancedLine(line={self.__line}, delimiter={self.__delimiter}, encoding={self.__encoding})"

    def __str__(self):
        return self.__line.decode(self.__encoding)

    def __bytes__(self):
        return self.__line

    def __eq__(self, other):
        return self.__line == other.__line

    def __len__(self):
        return len(self.__str__())

    def __getitem__(self, item: int):
        return self.__str__()[item]

    def __iter__(self):
        return self.__str__().__iter__()

    def __contains__(self, item):
        return item in self.__str__()

    def __add__(self, other):
        if isinstance(other, bytes):
            return self.__line + other
        elif isinstance(other, str):
            return self.__str__() + other
        elif isinstance(other, EnhancedLine):
            return self.__str__() + other.__str__()
        else:
            raise TypeError(f"Cannot concatenate {type(self)} with {type(other)}")

    @property
    def fields(self):
        return [EnhancedString(string.decode(self.__encoding)) for string in self.__line.split(self.__delimiter)]
