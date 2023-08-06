from src.containers import *
from src.image import Image
from pathlib import Path


class FileHeader:

    def __init__(self, path: Path):
        self.path = path
        self.file_name = path.name

        stem = path.stem
        file_name_info = stem.split("-")

        self.driver_id = file_name_info[0]
        self.date = file_name_info[1]
        self.time = file_name_info[2]

    def get_neighbor_image(self) -> Image:
        return Image(self.path.with_suffix(".jpg"))

    def open_as_network_output_container(self) -> NetworkOutputContainer:
        lines: list[str]
        with open(self.path, 'r') as file:
            lines = file.read().splitlines()
        network_output_container = NetworkOutputContainer.create_from_line_list(lines)
        return network_output_container

    def open_as_database_container(self) -> DatabaseContainer:
        lines: list[str]
        with open(self.path, 'r') as file:
            lines = file.readlines()
        database_container = DatabaseContainer.create_from_line_list(lines)
        return database_container

    def save_container(self, container: Container) -> None:
        container.save(self.path)
