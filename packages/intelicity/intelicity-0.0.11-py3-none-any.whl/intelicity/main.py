# import glob
# import time
# from pathlib import Path
#
# import pandas as pd
#
# class Ai_object:
#
#     def from_id(id):
#         return Ai_object()
#
#     def get_description(self):
#         return ""
#
#     def get_name(self):
#         return ""
#
#     def get_presentable_name(self):
#         return ""
#
#     @classmethod
#     def get_all_classes_indexes(cls):
#         return [i for i in range(0, 100)]
#
#
# class BruteTxtLine:
#     def __init__(self, line: str):
#
#         line_segments = line.rstrip().split(" ")
#
#         self.ai_object_id = int(line_segments[0])
#         self.bounding_box_x = line_segments[1]
#         self.bounding_box_y = line_segments[2]
#         self.bounding_box_width = line_segments[3]
#         self.bounding_box_height = line_segments[4]
#         self.score = float(line_segments[5])
#         self.class_name = line_segments[6]
#
#         def convert_string_to_float(x):
#             if x == "None":
#                 return None
#             else:
#                 return float(x)
#         self.latitude  = convert_string_to_float(line_segments[7])
#         self.longitude = convert_string_to_float(line_segments[8])
#
#     def get_coordinates(self):
#         return (self.latitude,self.longitude)
#
#     def is_coordinates_available(self):
#         return not ((self.latitude is None) or (self.longitude is None))
#
#     # def __init__(self, ai_object_id,bounding_box_x,bounding_box_y,bounding_box_width,bounding_box_height,score,class_name,latitude,longitude):
#     #
#     #     self.ai_object_id = ai_object_id
#     #     self.bounding_box_x = bounding_box_x
#     #     self.bounding_box_y = bounding_box_y
#     #     self.bounding_box_width = bounding_box_width
#     #     self.bounding_box_height = bounding_box_height
#     #     self.score = score
#     #     self.class_name = class_name
#     #     self.latitude = latitude
#     #     self.longitude = longitude
#
#     def to_str(self, has_line_break: bool = True) -> str:
#         line_break = "\n" if has_line_break else ""
#         return " ".join(vars(self).values()) + line_break
#         #return f"{self.ai_object_id} {self.bounding_box_x} {self.bounding_box_y} {self.bounding_box_width} {self.bounding_box_height} {self.score} {self.class_name} {self.latitude} {self.longitude}{line_break}"
#
#     def to_dict(self):
#         return vars(self)
#
# class BruteTxtFile:
#
#     def get_file(path):
#         return BruteTxtFile(path)
#
#     def get_files(glob_path : str) -> list["BruteTxtFile"]:
#         return [BruteTxtFile(file) for file in glob.glob(glob_path)]
#
#     def __init__(self, path):
#         if not isinstance(path, Path):
#             path = Path(path)
#
#         self.path = path
#         self.file_name = path.name
#         stem = path.stem
#         file_name_infos = stem.split("-")
#         self.driver_id = file_name_infos[0]
#         self.date = file_name_infos[1]
#         self.time = file_name_infos[2]
#         self.dataframe = None
#
#     def get_lines(self) -> list[BruteTxtLine]:
#         txt_lines = []
#         with open(self.path, "r") as file:
#             for line in file:
#                 brute_txt_line = BruteTxtLine(line)
#                 txt_lines.append(brute_txt_line)
#         return txt_lines
#
#     def create_dataframe(self):
#         lines = self.get_lines()
#         return pd.DataFrame([line.to_dict() for line in lines])
#
#     def get_classes_count(self):
#         dataframe = self.create_dataframe()
#         class_count = dataframe[["ai_object_id","class_name"]].groupby("ai_object_id").count()
#         class_count.index.name = None
#         class_count.name = None
#
#         class_count = class_count.to_dict()["class_name"]
#
#         #expected output
#         # {'11': 3, '24': 3}
#
#         return class_count
#
#     def adjust_coordinates(self):
#         pass
#
#     def remove_class_instances(self,ai_object_id):
#         pass
#
#     def insert_class_instances(self,txt_line):
#         pass
#
#     def save_as_txt(self,path):
#         pass
#
#     def replace_instances(self):
#         pass
#
#     def to_dict(self):
#         return {
#                 "driver_id":self.driver_id,
#                 "date": self.date,
#                 "time": self.time,
#                 }
#
#     def __repr__(self):
#         return f"BruteTxtFile({self.file_name})"
#
