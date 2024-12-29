"""base_class.py
"""

import json
from pathlib import Path
from typing import Dict, List, Union

# Type aliases
FilePathType = Union[str, Path]
Metadata = Dict[str, Union[str, int, float, List, Dict]]


class ExtractorBase:
    """Base class for all extractors.
    """

    def __call__(self, src: FilePathType, metadata: Metadata | None = None) -> Metadata:
        if isinstance(src, FilePathType):
            return self.process_file(src)
        if isinstance(src, Metadata):
            return self.process_data(src)
        raise TypeError(
            f"Unsupported type {type(src)} for src: Metadata or Path expected."
        )

    def process_file(self, src: FilePathType) -> Metadata:
        """Process the file and return the metadata.

        Args:
            src (FilePathType): The file to process.

        Returns:
            Metadata: The metadata.
        """
        src = json.loads(Path(src).read_text(encoding="utf-8"))
        return self.process_data(src)

    def process_data(self, src: Metadata) -> Metadata:
        """Process the data and return the metadata.

        Args:
            src (Metadata): The data to process.
            metadata (Metadata): The metadata to update.

        Returns:
            Metadata: The updated metadata.
        """
        raise NotImplementedError


class Converter:
    """Base class for all converters.
    """

    def __call__(self, src: FilePathType | Metadata) -> Metadata:
        if isinstance(src, FilePathType):
            return self.process_file(src)
        if isinstance(src, Metadata):
            return self.process_data(src)
        raise TypeError(
            f"Unsupported type {type(src)} for src: Metadata or Path expected."
        )

    def process_file(self, src: FilePathType) -> Metadata:
        """Process the file and return the metadata.

        Args:
            src (FilePathType): The file to process.

        Returns:
            Metadata: The metadata.
        """
        src = json.loads(Path(src).read_text(encoding="utf-8"))
        return self.process_data(src)

    def process_data(self, src: Metadata) -> Metadata:
        """Process the data and return the metadata.

        Args:
            src (Metadata): The data to process.
            metadata (Metadata): The metadata to update.

        Returns:
            Metadata: The updated metadata.
        """
        raise NotImplementedError


class OutputterBase:
    """Base class for all processors.
    """

    def __call__(self, src: FilePathType | Metadata, output_file_path: FilePathType) -> None:
        if isinstance(src, FilePathType):
            self.process_file(src, output_file_path)
        if isinstance(src, Metadata):
            self.process_data(src, output_file_path)
        raise TypeError(
            f"Unsupported type {type(src)} for src: Metadata or Path expected."
        )

    def process_file(self, src: FilePathType, output_file_path: FilePathType) -> None:
        """Process the file and return the metadata.

        Args:
            src (FilePathType): The file to process.

        Returns:
            Metadata: The metadata.
        """
        src = json.loads(Path(src).read_text(encoding="utf-8"))
        return self.process_data(
            Path(src).read_text(encoding="utf-8"), output_file_path
        )

    def process_data(self, src: Metadata, output_file_path: FilePathType) -> None:
        """Process the data and return the metadata.

        Args:
            src (Metadata): The data to process.
            metadata (Metadata): The metadata to update.

        Returns:
            Metadata: The updated metadata.
        """
        raise NotImplementedError
