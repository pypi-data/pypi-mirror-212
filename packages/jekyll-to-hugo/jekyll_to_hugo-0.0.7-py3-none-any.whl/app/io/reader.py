from abc import ABCMeta, abstractmethod


class IoReader(metaclass=ABCMeta):
    """
    Abstract class for reading posts.
    """

    @abstractmethod
    def read(self) -> str:
        """
        Reads a post.
        """
        raise NotImplementedError


class StringReader(IoReader):
    """
    Reads a post from a string.
    """

    def __init__(self, content: str):
        self._content = content

    def read(self) -> str:
        return self._content


class FileReader(IoReader):
    """
    Reads a post from a local file.
    """

    def __init__(self, file_path: str):
        self._file_path = file_path

    def read(self) -> str:
        with open(self._file_path, "r") as file:
            return file.read()
