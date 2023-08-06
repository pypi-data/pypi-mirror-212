import os
from pathlib import Path

import imagesize

from PIL import Image as Img

class Image:
    def __init__(self, jpg_path: Path):
        self.jpg_path = jpg_path

        width, height = imagesize.get(jpg_path)

        self.width = width
        self.height = height

    def is_corrupted(self):
        file_stats = os.stat(self.jpg_path)
        is_corrupted = (self.width == 0 or self.height == 0) or file_stats.st_size < 100
        return is_corrupted

    def open_image(self):
        try:
            # Replace this with code to open the image using an appropriate library

            im = Img.open(r"C:\Users\System-Pc\Desktop\ybear.jpg")
            im.show()

            return im
        except Exception as e:
            print(f"Error opening image: {str(e)}")

    def move_image(self, new_path: Path):
        import shutil
        try:
            shutil.move(self.jpg_path, new_path)
            # print(f"Image moved from '{self.path}' to '{new_path}' successfully.")
            self.jpg_path = new_path
        except FileNotFoundError:
            print(f"Error: Image file not found at {self.jpg_path}")

    def resize_image(self, new_width, new_height):
        # Code to resize the image to new_width and new_height
        # Replace this with appropriate image processing library functions
        print(f"Resized image '{self.jpg_path}' to {new_width}x{new_height}.")
        self.width = new_width
        self.height = new_height
