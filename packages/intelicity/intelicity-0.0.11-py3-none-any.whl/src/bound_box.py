import math


class BoundBox:
    def __init__(self, center_x: float | int, center_y: float | int, width: float | int, height: float | int):
        """
        Represents a bounding box with a center point, width, and height.

        Args:
            center_x (float | int): The x-coordinate of the center point.
            center_y (float | int): The y-coordinate of the center point.
            width (float | int): The width of the bounding box.
            height (float | int): The height of the bounding box.

        Raises:
            ValueError: If the width or height is negative or zero.
        """
        if width < 0 or height < 0:
            raise ValueError("Width and height must be non-negative.")
        if width == 0 or height == 0:
            raise ValueError("Width and height must be greater than zero.")

        self._center_x = center_x
        self._center_y = center_y
        self._width = width
        self._height = height

    @property
    def left(self) -> float | int:
        """The x-coordinate of the left edge of the bounding box."""
        return self._center_x - (self._width / 2)

    @property
    def right(self) -> float | int:
        """The x-coordinate of the right edge of the bounding box."""
        return self._center_x + (self._width / 2)

    @property
    def top(self) -> float | int:
        """The y-coordinate of the top edge of the bounding box."""
        return self._center_y - (self._height / 2)

    @property
    def bottom(self) -> float | int:
        """The y-coordinate of the bottom edge of the bounding box."""
        return self._center_y + (self._height / 2)

    @property
    def center_x(self) -> float | int:
        """The x-coordinate of the center point of the bounding box."""
        return self._center_x

    @property
    def center_y(self) -> float | int:
        """The y-coordinate of the center point of the bounding box."""
        return self._center_y

    @property
    def width(self) -> float | int:
        """The width of the bounding box."""
        return self._width

    @property
    def height(self) -> float | int:
        """The height of the bounding box."""
        return self._height

    def get_area(self) -> float | int:
        """Calculates the area of the bounding box."""
        return self._width * self._height

    def intersects(self, other_box: 'BoundBox') -> bool:
        """
        Checks if this bounding box intersects with another bounding box.

        Args:
            other_box (BoundBox): The other bounding box to check against.

        Returns:
            bool: True if the bounding boxes intersect, False otherwise.
        """
        return not (self.right < other_box.left or
                    self.left > other_box.right or
                    self.bottom < other_box.top or
                    self.top > other_box.bottom)

    def contains_point(self, point_x: float, point_y: float) -> bool:
        """
        Checks if the bounding box contains a given point.

        Args:
            point_x (float): The x-coordinate of the point.
            point_y (float): The y-coordinate of the point.

        Returns:
            bool: True if the point is inside the bounding box, False otherwise.
        """
        return (self.left <= point_x <= self.right and
                self.top <= point_y <= self.bottom)

    def to_pixel_space(self, screen_width: float, screen_height: float) -> 'BoundBox':
        """
        Converts the bounding box from normalized coordinates to pixel coordinates.

        Args:
            size_x (float): The size of the x-axis in pixel units.
            size_y (float): The size of the y-axis in pixel units.

        Returns:
            BoundBox: A new BoundBox instance representing the bounding box in pixel space.
        """
        pixel_width = int(self._width * screen_width)
        pixel_height = int(self._height * screen_height)
        pixel_center_x = int(self._center_x * screen_width)
        pixel_center_y = int(self._center_y * screen_height)

        return BoundBox(pixel_center_x, pixel_center_y, pixel_width, pixel_height)

    def to_screen_space(self, screen_width: float, screen_height: float) -> 'BoundBox':
        """
        Converts the bounding box from pixel coordinates to normalized coordinates.

        Args:
            size_x (float): The size of the x-axis in pixel units.
            size_y (float): The size of the y-axis in pixel units.

        Returns:
            BoundBox: A new BoundBox instance representing the bounding box in normalized screen space.
        """

        if screen_width <= 0 or screen_height <= 0:
            raise ValueError("Width and height must be greater than zero.")

        screen_center_x = self._center_x / screen_width
        screen_center_y = self._center_y / screen_height
        screen_width = self._width / screen_width
        screen_height = self._height / screen_height

        return BoundBox(screen_center_x, screen_center_y, screen_width, screen_height)

    def get_xyxy(self) -> tuple[float | int, float | int, float | int, float | int]:
        """Returns the bounding box coordinates in the format (x_min, y_min, x_max, y_max)."""
        x_min = self.left
        y_min = self.top
        x_max = self.right
        y_max = self.bottom
        return x_min, y_min, x_max, y_max

    def __str__(self) -> str:
        """Returns a string representation of the bounding box."""
        return f"{self._center_x} {self._center_y} {self._width} {self._height}"

    def __repr__(self) -> str:
        """Returns a string representation of the bounding box."""
        return f"BoundBox({str(self)})"

    def __eq__(self, other: object) -> bool:
        """
        Checks if this bounding box is equal to another bounding box.

        Args:
            other (object): The other object to compare.

        Returns:
            bool: True if the bounding boxes are equal, False otherwise.
        """
        if isinstance(other, BoundBox):
            return (math.isclose(self.center_x, other.center_x) and
                    math.isclose(self.center_y, other.center_y) and
                    math.isclose(self.width, other.width) and
                    math.isclose(self.height, other.height))
        return False
