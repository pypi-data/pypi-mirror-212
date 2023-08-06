from math import sin, cos, acos


class GeoLocation:
    """
    A class representing a geographic location with latitude and longitude coordinates.
    """

    @classmethod
    def create_from_string(cls, string1: str, string2: str) -> "GeoLocation":
        """
        Create a GeoLocation instance from latitude and longitude strings.

        Args:
            string1 (str): The string representing the latitude coordinate.
            string2 (str): The string representing the longitude coordinate.

        Returns:
            GeoLocation: The created GeoLocation instance.
        """
        value1 = None
        if string1 != "None":
            value1 = float(string1)

        value2 = None
        if string2 != "None":
            value2 = float(string2)

        return cls(value1, value2)

    def __init__(self, latitude, longitude):
        """
        Initialize a GeoLocation instance.

        Args:
            latitude (float or None): The latitude coordinate.
            longitude (float or None): The longitude coordinate.
        """

        self.latitude = latitude
        self.longitude = longitude

    def is_valid_coordinate(self) -> bool:
        """
        Check if the latitude and longitude coordinates are valid.

        Returns:
            bool: True if the coordinates are valid, False otherwise.
        """
        return not (self.latitude is None or self.longitude is None)

    def get_distance_to(self, other_location: "GeoLocation") -> float:
        """
        Calculate the distance between two GeoLocation instances using the Haversine formula.

        Args:
            other_location (GeoLocation): The other GeoLocation instance.

        Returns:
            float: The distance between the two locations in kilometers.
        """
        return acos(
            sin(self.latitude) * sin(other_location.latitude) + cos(self.latitude) * cos(other_location.latitude) * cos(
                other_location.longitude - self.longitude)) * 6371

    def __str__(self):
        """
        Return the string representation of the GeoLocation instance.

        Returns:
            str: The string representation of the GeoLocation instance.
        """
        return f"{self.latitude} {self.longitude}"

    def __eq__(self, other: "GeoLocation"):
        """
        Check if two GeoLocation instances are equal.

        Args:
            other (GeoLocation): The other GeoLocation instance.

        Returns:
            bool: True if the two GeoLocation instances are equal, False otherwise.
        """
        return self.latitude == other.latitude and self.longitude == other.longitude

