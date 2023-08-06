from pathlib import Path
from intelicity.contents import *


class Container:

    def __init__(self, contents: list[FileContent]):
        self.contents = contents
        pass

    def save(self, path: Path) -> None:
        with open(path, 'w') as file:
            for file_content in self.contents:
                file.write(str(file_content)+"\n")


class NetworkOutputContainer(Container):
    @classmethod
    def create_from_line_list(cls, lines: list[str]) -> "NetworkOutputContainer":
        contents = [NetworkOutputContent.create_from_line(line) for line in lines]
        return NetworkOutputContainer(contents)

    def __init__(self, contents: list[NetworkOutputContent]):
        super().__init__(contents)

    def concatenate(self, network_output_container: "NetworkOutputContainer") -> None:
        """
        concatenate 2 NetworkOutputContainer together on the first one
        """

        self.contents = self.contents + network_output_container.contents

    def convert_to_database_container(self, screen_width: float, screen_height: float, geo_location: GeoLocation):
        new_contents: list[DatabaseContent] = []

        content: NetworkOutputContent
        for content in self.contents:
            new_contents.append(content.convert_to_database(screen_width, screen_height, geo_location))

        database_container = DatabaseContainer(new_contents)

        return database_container

    def __eq__(self, other):
        if not isinstance(other, NetworkOutputContainer):
            return False
        return self.contents == other.contents
    def add(self, network_output_content: NetworkOutputContent) -> None:
        self.contents.append(network_output_content)


class DatabaseContainer(Container):

    @classmethod
    def create_from_line_list(cls, lines: list[str]) -> "DatabaseContainer":
        contents = [DatabaseContent.create_from_line(line) for line in lines]
        return cls(contents)

    # @classmethod
    # def create_from_values(cls, lines: list[str], latitude: float, longitude: float) -> "DatabaseContainer":
    #     contents = [DatabaseContent.create_from_line(lines,latitude,longitude) for line in lines]
    #     latitude = latitude
    #     longitude = longitude
    #
    #     return cls(contents, latitude, longitude)

    def __init__(self, contents: list[DatabaseContent]):
        super().__init__(contents)

    def __eq__(self, other):
        if not isinstance(other, DatabaseContainer):
            return False
        return self.contents == other.contents

    def concatenate(self, database_container: "DatabaseContainer") -> None:
        """
        concatenate 2 DatabaseContainers together on the first one
        """
        for content in database_container.contents:
            self.contents.append(content)

    def convert_to_network_output_container(self, screen_width, screen_height):
        new_contents: list[NetworkOutputContent] = []


        content: DatabaseContent
        for content in self.contents:
            new_contents.append(content.convert_to_network_output(screen_width, screen_height))

        network_output_container = NetworkOutputContainer(new_contents)

        return network_output_container

    def add(self, database_content: DatabaseContent) -> None:
        self.contents.append(database_content)
