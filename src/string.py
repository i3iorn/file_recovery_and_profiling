class EnhancedString:
    def __init__(self, string: str):
        self.__string = string

    def __repr__(self):
        return f"EnhancedString(string={self.__string})"

    def __str__(self):
        return self.__string

    def __eq__(self, other):
        return self.__string == other.__string

    def __len__(self):
        return len(self.__string)

    def __getitem__(self, item: int):
        return self.__string[item]

    def __iter__(self):
        return self.__string.__iter__()

    def __contains__(self, item):
        return item in self.__string

    def __hash__(self):
        return hash(self.__string)