import os
from enum import Enum
from io import BytesIO
from zipfile import ZipFile

from src.converters import XlsxToCsvConverter, RtfToCsvConverter, PdfToCsvConverter, DocxToCsvConverter, \
    DocToCsvConverter
from src.file_content_object import FileContent


class FileType(Enum):
    XLS = b'\xd0\xcf\x11\xe0'
    XLSX = b'\x50\x4b\x03\x04'
    ZIP = b'PK\x03\x04'
    RTF = b'\x7b\x5c\x72\x74'
    PDF = b'%PDF'
    DOC = b'\xd0\xcf\x11\xe0'
    DOCX = b'PK\x03\x04'
    TEXT = b''


class FileTypeException(Exception):
    pass


class FileManager:
    """
    File Manager Class

    Takes a file, folder, list of files, or list of folders and returns a list of content strings.
    """
    EXTENSIONS = ['txt', 'csv']

    def __init__(self, path: str = None, paths: list = None, recursive: bool = False, extensions: list = None):
        # Validate input
        if path is None and paths is None:
            raise ValueError("Must provide a path or list of paths.")
        if recursive is not None and not isinstance(recursive, bool):
            raise TypeError("Recursive must be a boolean.")
        if extensions is not None and not isinstance(extensions, list):
            raise TypeError("Extensions must be a list.")

        # Initialize variables
        self.__index = 0
        self.__paths = []
        if path is not None:
            self.__paths.append(path)
        if paths is not None:
            self.__paths.extend(paths)

        # Validate paths
        for path in self.__paths:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Path '{path}' does not exist.")
            if not os.path.isdir(path) and not os.path.isfile(path):
                raise ValueError(f"Path '{path}' is not a file or folder.")

        # Get all files from supplied paths
        self.__files = []
        for path in self.__paths:
            if os.path.isdir(path):
                self.__files.extend(self.__get_files_from_folder(path, recursive, extensions or self.EXTENSIONS))
            else:
                self.__files.append(path)

        # Get content from all files
        self.__content = []
        for file in self.__files:
            with open(file, 'rb') as f:
                content = f.read()
                ft = self.__file_type_by_content(content[:100])
                if ft == FileType.ZIP:
                    for file_content in self.__get_files_from_zip(content):
                        ft = self.__file_type_by_content(file_content[:100])
                        self.__content.append(self.__get_content_object(ft, file_content))
                else:
                    self.__content.append(self.__get_content_object(ft, content))
                self.__content[-1].properties.file_type = ft

    @property
    def content(self):
        return self.__content

    @staticmethod
    def __get_files_from_folder(path, recursive: bool = False, extensions: list = None):
        files = []
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                if extensions is None or len(extensions) == 0:
                    files.append(os.path.join(root, filename))
                elif filename.split('.')[-1] in extensions:
                    files.append(os.path.join(root, filename))
            if not recursive:
                break
        return files

    def __repr__(self):
        return f"FileManager(paths={self.__paths}, files={self.__files}, content={self.__content})"

    def __iter__(self):
        return self.__content.__iter__()

    def __next__(self):
        if self.__index < len(self.__content):
            result = self.__content[self.__index]
            self.__index += 1
            return result
        else:
            self.__index = 0
            raise StopIteration

    @staticmethod
    def __file_type_by_content(start_bytes):
        """
        Returns the file type based on the first 4 bytes of the file.
        """
        for ft in FileType:
            if start_bytes.startswith(ft.value):
                return ft
        return FileTypeException(f'Unable to determine filetype')

    @staticmethod
    def __get_content_object(ft, content):
        """
        Returns a FileContent object based on the file type.
        """
        if ft == FileType.XLS:
            converted_content = XlsxToCsvConverter(content)
        elif ft == FileType.XLSX:
            converted_content = XlsxToCsvConverter(content)
        elif ft == FileType.TEXT:
            converted_content = content
        else:
            raise ValueError(f"File type '{ft}' is not supported.")
        return FileContent(converted_content)

    @staticmethod
    def __get_files_from_zip(zipped_content):
        """
        Returns a list of files from a zip file.
        """
        unzipped_files_content = []
        with ZipFile(BytesIO(zipped_content)) as zip_file:
            for file in zip_file.namelist():
                unzipped_files_content.append(zip_file.open(file).read())

        return unzipped_files_content
