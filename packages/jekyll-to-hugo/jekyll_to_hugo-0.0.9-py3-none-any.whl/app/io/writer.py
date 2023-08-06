from abc import ABCMeta, abstractmethod
from pathlib import Path

from app import utils


class IoWriter(metaclass=ABCMeta):
    """
    Abstract class for writing posts.
    """

    @abstractmethod
    def write(self, data: str):
        """
        Write a post

        Parameters
        ----------
        data: str
            The post data to write
        """
        raise NotImplementedError


class FileWriter(IoWriter):
    """
    Writes a post to a file.
    """

    def __init__(self, output_path: Path):
        utils.guard_against_none(output_path, "output_path")

        self.output_path = output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, data: str):
        with open(self.output_path, "w") as fo:
            fo.write(data)


class MockWriter(IoWriter):
    """
    Writes a post to a string.
    """

    def __init__(self):
        self.content = ""

    def write(self, data: str):
        self.content += data
