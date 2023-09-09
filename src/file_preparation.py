from enum import Enum
from zipfile import ZipFile


class FileType(Enum):
    TEXT = b''
    XLS = b'\xd0\xcf\x11\xe0'
    XLSX = b'\x50\x4b\x03\x04'
    ZIP = b'PK\x03\x04'
    RTF = b'\x7b\x5c\x72\x74'


class FilePreparation:
    """
    Class for preparing files for further processing. It takes a file, folder, or list of files and folders. It first
    stores all file contents as bytes. Then it checks the file type and converts it to a text file. It then stores the
    text file contents as an utf8 encoded string.
    """
    def __init__(self, file: str = None, folder: str = None, file_list: list = None):
        # Check that atleast one parameter is given
        if not any([file, folder, file_list]):
            raise ValueError("At least one parameter must be given.")

        # Check that only one parameter is given
        if sum([bool(file), bool(folder), bool(file_list)]) > 1:
            raise ValueError("Only one parameter must be given.")

        # Check that the given parameter is of the correct type
        if file and not isinstance(file, str):

