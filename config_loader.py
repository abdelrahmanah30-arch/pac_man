import json

class Configloader:
    def __init__(self, config_path):
        self.config_path = config_path
        self.file_list = []

    def load(self):
        with open(self.config_path, "r") as file_object:
            read_file = file_object.readline()
            while read_file != "":

                if not read_file.lstrip().startswith("#"):
                    self.file_list.append(read_file)
                read_file = file_object.readline()

            specifoc_json = "".join(self.file_list)
            try:
                config_data = json.loads(specifoc_json)
                return config_data
            except json.JSONDecodeError as error:
                print(error)


class ConfigValidator:
    def __init__(self, config_data: dict):
        self.config_data = config_data
        self.config_level = []

    def validate(self):
        try:
            for key, value in self.config_data.items():
                if key == "level":
                    for item in self.config_data[key]:
                        if isinstance(item, int):
                            if not item < 1 and not item > 10:
                                self.config_level.append(item)

                    for item in range(10):
                        if not (item + 1) in self.config_level:
                            self.config_level.append(item + 1)

                    self.config_level.sort()
                    
                        
            if "lives" not in self.config_data:
                self.config_data["lives"] = 3

            if not isinstance(self.config_data["lives"], int):
                self.config_data["lives"] = 3

            if "lives" in self.config_data:
                if self.config_data["lives"] < 1:
                    self.config_data["lives"] = 3
                elif self.config_data["lives"] > 3:
                    self.config_data["lives"] = 3

            if "width" not in self.config_data:
                self.config_data["width"] = 21

            if "height" not in self.config_data:
                self.config_data["height"] = 21

            if not isinstance(self.config_data["width"], int):
                    self.config_data["width"] = 21

            if not isinstance(self.config_data["height"], int):
                self.config_data["height"] = 21

            if "width" in self.config_data:
                if self.config_data["width"] < 5:
                    self.config_data["width"] = 21
                elif self.config_data["width"] > 50:
                    self.config_data["width"] = 21

            if "height" in self.config_data:
                if self.config_data["height"] < 5:
                    self.config_data["height"] = 21
                elif self.config_data["height"] > 50:
                    self.config_data["height"] = 21

            if "pacgum" not in self.config_data:
                self.config_data["pacgum"] = 42

            if not isinstance(self.config_data["pacgum"], int):
                self.config_data["pacgum"] = 42

            if "pacgum" in self.config_data:
                if self.config_data["pacgum"] < 1:
                    self.config_data["pacgum"] = 42

            if "points_per_pacgum" not in self.config_data:
                self.config_data["points_per_pacgum"] = 10

            if not isinstance(self.config_data["points_per_pacgum"], int):
                self.config_data["points_per_pacgum"] = 10

            if "points_per_pacgum" in self.config_data:
                if self.config_data["points_per_pacgum"] < 0:
                    self.config_data["points_per_pacgum"] = 10

            if "points_per_super_pacgum" not in self.config_data:
                self.config_data["points_per_super_pacgum"] = 50

            if not isinstance(self.config_data["points_per_super_pacgum"], int):
                self.config_data["points_per_super_pacgum"] = 50

            if "points_per_super_pacgum" in self.config_data:
                if self.config_data["points_per_super_pacgum"] < 0:
                    self.config_data["points_per_super_pacgum"] = 50

            if "points_per_ghost" not in self.config_data:
                self.config_data["points_per_ghost"] = 200

            if not isinstance(self.config_data["points_per_ghost"], int):
                self.config_data["points_per_ghost"] = 200

            if "points_per_ghost" in self.config_data:
                if self.config_data["points_per_ghost"] < 0:
                    self.config_data["points_per_ghost"] = 200

            if "seed" not in self.config_data:
                self.config_data["seed"] = 42

            if not isinstance(self.config_data["seed"], int):
                self.config_data["seed"] = 42

            if "seed" in self.config_data:
                if self.config_data["seed"] < 0:
                    self.config_data["seed"] = 42

            if "level_max_time" not in self.config_data:
                self.config_data["level_max_time"] = 90

            if not isinstance(self.config_data["level_max_time"], int):
                self.config_data["level_max_time"] = 90

            if "level_max_time" in self.config_data:
                if self.config_data["level_max_time"] < 1:
                    self.config_data["level_max_time"] = 90

        except ValueError as error:
            print(error)