from pathlib import Path

from intelicity.file_header import FileHeader


class FolderHeader:

    def __init__(self, path: Path):
        self.path = path
        self.folder_name = path.name

    def get_file_headers(self):
        return [FileHeader(path) for path in self.path.glob("*.txt")]