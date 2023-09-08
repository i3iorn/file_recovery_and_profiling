from pathlib import Path

from charset_normalizer import from_bytes

from src.converters import ExcelConverter
from src.line import EnhancedLine


class EnhancedFile:
    BYTES_TO_ANALYZE = 8192
    LINES_TO_ANALYZE = 50
    LINE_BREAKS = [b'\r\n', b'\r', b'\n']

    def __init__(self, path_string: str):
        self.__index = 0
        self.__headers = None

        with open(path_string, 'rb') as f:
            self.__original_content = f.read()
        self.__content = self.__original_content
        self.__sample = self.__content[:self.BYTES_TO_ANALYZE]

        self.__path_string = self.__validate_path(path_string)
        self.__path_object = Path(self.__path_string)
        self.__properties = FileProperties(self.__sample)
        self.__lines = self.__get_lines()

    def __enter__(self):
        self.file_pointer = open(self.__path_string, 'rb')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file_pointer.close()

    def __iter__(self):
        return self

    def __eq__(self, other):
        return self.properties == other.properties

    def __next__(self):
        if self.__index < len(self.__lines):
            line = self.__lines[self.__index]
            self.__index += 1
            return line
        else:
            self.__index = 0
            raise StopIteration

    def __len__(self):
        return len(self.__lines)

    def __repr__(self):
        return f"EnhancedFile(path={self.__path_string}, encoding={self.__properties.encoding}, " \
               f"line_break={self.__properties.line_break}, delimiter={self.__properties.delimiter})"

    @staticmethod
    def __validate_path(path_string: str):
        if not isinstance(path_string, str):
            raise TypeError(f"Path must be a string, not {type(path_string)}")

        path = Path(path_string)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {path_string}")

        if not path.is_file():
            raise FileNotFoundError(f"Path is not a file: {path_string}")

        if path.suffix in ['.xlsx', '.xls']:
            ec = ExcelConverter(path_string)
            path_string = ec.to_csv()

        return path_string

    @property
    def content(self):
        return self.__content

    @property
    def properties(self):
        return self.__properties

    @content.setter
    def content(self, value):
        self.__content = value

    @property
    def headers(self):
        if not hasattr(self, '__headers'):
            self.__headers = self.__get_first_row()
        return self.__headers

    @property
    def unique_columns(self):
        return self.get_unique_columns()

    def __get_lines(self):
        return [EnhancedLine(li, delimiter=self.properties.delimiter, encoding=self.properties.encoding)
            for li in self.__content.split(self.__properties.line_break)]

    def __get_first_row(self):
        headers = self.__content.split(self.__properties.line_break)[0].split(self.__properties.delimiter)

        if len(headers) != len(set(headers)):
            raise ValueError("Headers are not unique.")

        if len(headers) != len([h for h in headers if h != b'']):
            raise ValueError("Headers cannot be empty.")

        for i, header in enumerate(headers):
            if header.decode(self.__properties.encoding).isnumeric():
                raise ValueError(f"Headers cannot be numeric. ({header})")

        return headers

    # find columns with unique values
    def get_unique_columns(self):
        unique_columns = []
        for i in range(len(self.headers)):
            column = self.get_column(i)
            if len(set(column)) == len(column):
                unique_columns.append(i)
        return unique_columns

    @classmethod
    def repair(cls, path_string: str):
        rep_file = cls(path_string)
        rep_file_path = Path(path_string).with_suffix('.repaired')
        with open(rep_file_path, 'wb') as f:
            f.write(rep_file.content)

        if path_string.endswith('.xlsx') or path_string.endswith('.xls'):
            ec = ExcelConverter(str(rep_file_path.absolute()), preserve_extension=True)
            excel_path = ec.to_excel()
            return excel_path
        return rep_file_path

    def get_column(self, i):
        return [line.fields[i] for line in self.__lines[:self.LINES_TO_ANALYZE] if len(line.fields) > i]


class FileProperties:
    LINE_BREAKS = [b'\r\n', b'\r', b'\n']
    DELIMITERS = [b';', b',', b'\t', b'|', b':']
    STRING_QUALIFIERS = [b'"', b"'"]

    def __init__(self, sample: bytes):
        self.line_break = self.__detect_linebreaks(sample)
        self.encoding = from_bytes(sample).best().encoding
        self.delimiter = max(self.DELIMITERS, key=sample.count)

    def __detect_linebreaks(self, sample):
        count = [sample.count(b) for b in self.LINE_BREAKS]
        if len(count) == len(set(count)):
            return self.LINE_BREAKS[count.index(min(count))]
        elif len(set(count)) == 1:
            return b'\r\n'
        elif len(set(count)) == 2:
            return [lb for lb, c in zip(self.LINE_BREAKS, count) if c == min(count)][0]
