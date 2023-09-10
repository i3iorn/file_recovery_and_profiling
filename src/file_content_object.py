from charset_normalizer import from_bytes


class Line:
    def __init__(self, line, properties):
        self.__index = 0
        self.__line = line
        self.__properties = properties
        self.__fields = self.__get_fields()

    def __iter__(self):
        return self.__fields.__iter__()

    def __next__(self):
        if self.__index < len(self.fields):
            field = self.fields[self.__index]
            self.__index += 1
            return field
        else:
            self.__index = 0
            raise StopIteration

    def __repr__(self):
        return self.__line

    def __str__(self):
        return self.__line.decode(self.__properties.encoding)

    def __get_fields(self):
        return [f.replace(self.__properties.string_qualifier, b'').decode(self.__properties.encoding) for f in self.__line.split(self.__properties.delimiter)]

    @property
    def fields(self):
        return self.__fields


class FileProperties:
    LINE_BREAKS = [b'\r\n', b'\r', b'\n']
    DELIMITERS = [b';', b',', b'\t', b'|', b':']
    STRING_QUALIFIERS = [b'"', b"'"]

    def __init__(self,
                 sample: bytes,
                 delimiter: bytes = None,
                 encoding: str = None,
                 line_break: bytes = None,
                 ):
        self.line_break = line_break or self.__detect_linebreaks(sample)
        self.encoding = encoding or from_bytes(
            sample, cp_isolation=['iso-8859-1', 'utf-8', 'windows-1252']
        ).best().encoding
        self.delimiter = delimiter or max(self.DELIMITERS, key=sample.count)
        self.string_qualifier = self.__detect_string_qualifier(sample)

    def __detect_linebreaks(self, sample):
        count = [sample.count(b) for b in self.LINE_BREAKS]
        if len(count) == len(set(count)):
            return self.LINE_BREAKS[count.index(min(count))]
        elif len(set(count)) == 1:
            return b'\r\n'
        elif len(set(count)) == 2:
            return [lb for lb, c in zip(self.LINE_BREAKS, count) if c == min(count)][0]

    def __repr__(self):
        return (f"FileProperties("
                f"line_break={self.line_break}, "
                f"encoding={self.encoding}, "
                f"delimiter={self.delimiter}, "
                f"string_qualifier={self.string_qualifier})")

    def __detect_string_qualifier(self, sample):
        count = [sample.count(b) for b in self.STRING_QUALIFIERS]
        if len(count) == len(set(count)):
            return self.STRING_QUALIFIERS[count.index(max(count))]
        elif len(set(count)) == 1:
            return b''
        elif len(set(count)) == 2:
            return [lb for lb, c in zip(self.STRING_QUALIFIERS, count) if c == min(count)][0]


class FileContent:
    """
    Takes the content of a file in bytes and cretes a normalized object for it.
    """

    BYTES_TO_ANALYZE = 8192
    LINES_TO_ANALYZE = 100

    def __init__(self, content: bytes):
        self.__index = 0
        self.__raw_content = content
        self.__properties = FileProperties(content[:self.BYTES_TO_ANALYZE])
        self.__str_content = self.__raw_content.decode(self.__properties.encoding)
        self.__lines = self.__get_lines()

    def __repr__(self):
        return self.__raw_content

    def __str__(self):
        return self.__raw_content.decode(self.__properties.encoding)

    @property
    def lines(self):
        return self.__lines

    @property
    def properties(self):
        return self.__properties

    def get_column(self, column_index):
        return [line.fields[column_index] for line in self.__lines]


    def __get_lines(self):
        return [Line(line, self.properties) for line in self.__raw_content.split(self.__properties.line_break) if len(line) > 0]

    def __iter__(self):
        return self.__lines.__iter__()

    def __len__(self):
        return len(self.__lines)

    def __getitem__(self, item: int):
        return self.__lines[item]

    def __next__(self):
        if self.__index < len(self.__lines):
            result = self.__lines[self.__index]
            self.__index += 1
            return result
        else:
            self.__index = 0
            raise StopIteration
