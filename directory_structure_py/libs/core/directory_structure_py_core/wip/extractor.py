"""extractor.py: Extracts the directory structure of a given directory.
"""

from directory_structure_py.libs.core.directory_structure_py_core.wip.base_class import ExtractorBase, Metadata, FilePathType


class FileMetadataExtractor(ExtractorBase):
    """Extracts the metadata of a given file.
    """

    def process_file(self, src: FilePathType) -> Metadata:
        """Process the file and return the metadata.

        Args:
            src (FilePathType): The file to process.

        Returns:
            Metadata: The metadata.
        """
        raise NotImplementedError

    def process_data(self, src: Metadata) -> Metadata:
        """Process the data and return the metadata.

        Args:
            src (Metadata): The data to process.

        Returns:
            Metadata: The updated metadata.
        """
        fpath: str = src.get("@id")
        raise NotImplementedError

class DirectoryMetadataExtractor(ExtractorBase):
    """Extracts the directory metadata of a given directory.
    """

    def process_data(self, src: Metadata) -> Metadata:
        """Process the data and return the metadata.

        Args:
            src (Metadata): The data to process.

        Returns:
            Metadata: The updated metadata.
        """
        raise NotImplementedError