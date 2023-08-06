from src.ai_object import AiObject
from src.bound_box import BoundBox
from src.geo_location import GeoLocation


class FileContent:
    pass


class DatabaseContent(FileContent):
    """
        representation of a line of a .txt file that is output of an Ai network\n
        \n
        Example is:\n
        1 933 675 671 466 0.704676 Valeta -23.6383339 -46.7367179\n
        Correspond to:\n
        [0] ai_object\n
        [1] pixel_space_center_x \n
        [2] pixel_space_center_y\n
        [3] pixel_space_size_x\n
        [4] pixel_space_size_y\n
        [5] trust\n
        [6] ai_object_name\n
        [7] latitude\n
        [8] longitude\n
    """
    @classmethod
    def create_from_line(cls, string: str):

        segments = cls.parse(string)

        ai_object = AiObject.create_from_global_id(int(segments[0]))
        pixel_space_center_x = int(segments[1])
        pixel_space_center_y = int(segments[2])
        pixel_space_size_x = int(segments[3])
        pixel_space_size_y = int(segments[4])
        trust = float(segments[5])

        geo_location = GeoLocation.create_from_string(segments[7], segments[8])
        pixel_bound_box = BoundBox(pixel_space_center_x, pixel_space_center_y, pixel_space_size_x, pixel_space_size_y)

        return cls(ai_object, pixel_bound_box, trust, geo_location)

    def __init__(self, ai_object: AiObject, pixel_bound_box: BoundBox, trust: float, geo_location: GeoLocation):
        if (type(ai_object) == str):
            raise ValueError("ai_object should be an AiObject, not a string, may use database_content.create_from_line()")

        self.ai_object = ai_object
        self.pixel_bound_box = pixel_bound_box
        self.trust = trust
        self.geo_location = geo_location

    def get_ai_object_name(self):
        return AiObject.get_object_name(ai_id=self.ai_object.ai_id)

    def __str__(self):
        return f"{self.ai_object.get_global_id()} {str(self.pixel_bound_box)} {self.trust} {self.get_ai_object_name()} {str(self.geo_location)}"

    def __repr__(self):
        return f"DatabaseContent({str(self)})"
    def __eq__(self, other: "DatabaseContent"):
        if not isinstance(other, DatabaseContent):
            return False
        return self.ai_object == other.ai_object and self.pixel_bound_box == other.pixel_bound_box and self.trust == other.trust and self.geo_location == other.geo_location
    def get_pixel_space_xyxy(self) -> tuple[int, int, int, int]:
        return self.pixel_bound_box.get_xyxy()

    def convert_to_network_output(self, screen_width, screen_height) -> "NetworkOutputContent":
        bound_box = self.pixel_bound_box.to_screen_space(screen_width, screen_height)
        return NetworkOutputContent(self.ai_object, bound_box, self.trust)

    @classmethod
    def parse(cls, string) -> list[str]:
        # Remove leading and trailing whitespaces
        string = string.strip()

        # Raise an error if the line starts with a space
        if string.startswith(' '):
            raise ValueError("Input string should not start with a space.")

        # Raise an error if the line ends with a line break or empty space
        if string.endswith('\n') or string.endswith(' '):
            raise ValueError("Input string should not end with a line break or empty space.")

        segments = string.split(" ")

        # Define the expected count of segments
        expected_count = 9

        # Raise an error if the number of segments doesn't match the expected count
        if len(segments) != expected_count:
            raise ValueError(f"Expected {expected_count} segments, but found {len(segments)}.")

        return segments


class NetworkOutputContent(FileContent):
    """
        representation of a line of a .txt file that is output of an Ai network\n
        \n
        exemple is:\n
        1 0.730469 0.719792 0.539062 0.48125 0.649228\n
        correspond to:\n
        [0] ai_object\n
        [1] screen_space_center_x\n
        [2] screen_space_center_y\n
        [3] screen_space_size_x\n
        [4] screen_space_size_y\n
        [5] trust\n
    """

    def __init__(self, ai_object: AiObject, screen_bound_box: BoundBox, trust: float):

        if (type(ai_object) == str):
            raise ValueError("ai_object should be an AiObject, not a string, may use NetworkOutputContent.create_from_line()")

        self.ai_object = ai_object
        self.screen_bound_box = screen_bound_box
        self.trust = trust

    @classmethod
    def create_from_line(cls, string: str) -> "NetworkOutputContent":

        segments = cls.parse(string)

        ai_object = AiObject.create_from_global_id(int(segments[0]))
        screen_space_center_x = float(segments[1])
        screen_space_center_y = float(segments[2])
        screen_space_size_x = float(segments[3])
        screen_space_size_y = float(segments[4])
        trust = float(segments[5])

        screen_bound_box = BoundBox(screen_space_center_x, screen_space_center_y, screen_space_size_x, screen_space_size_y)
        return cls(ai_object, screen_bound_box, trust)

    def __str__(self):
        return f"{self.ai_object.get_global_id()} {str(self.screen_bound_box)} {self.trust}"

    def __repr__(self):
        return f"NetworkOutput({str(self)})"

    def __eq__(self, other):
        if isinstance(other, NetworkOutputContent):
            return self.ai_object == other.ai_object and self.screen_bound_box == other.screen_bound_box and self.trust == other.trust
        return False

    def convert_to_database(self, screen_width: float, screen_height: float, geo_location: GeoLocation) -> DatabaseContent:
        bound_box = self.screen_bound_box.to_pixel_space(screen_width, screen_height)
        return DatabaseContent(self.ai_object, bound_box, self.trust, geo_location)

    @classmethod
    def parse(cls, string) -> list[str]:
        # Remove leading and trailing whitespaces
        string = string.strip()

        # Raise an error if the line starts with a space
        if string.startswith(' '):
            raise ValueError("Input string should not start with a space.")

        # Raise an error if the line ends with a line break or empty space
        if string.endswith('\n') or string.endswith(' '):
            raise ValueError("Input string should not end with a line break or empty space.")

        segments = string.split(" ")

        # Define the expected count of segments
        expected_count = 6

        # Raise an error if the number of segments doesn't match the expected count
        if len(segments) != expected_count:
            raise ValueError(f"Expected {expected_count} segments, but found {len(segments)}.")

        return segments



