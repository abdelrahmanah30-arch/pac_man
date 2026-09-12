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
            print("#######")
            print(specifoc_json)
            print("#######")
            try:
                print("converte to json")
                config_data = json.loads(specifoc_json)
                print(config_data["highscore_filename"])
                print(config_data["level"])
                print(type(config_data))
                print(type(config_data["highscore_filename"]))
                print(type(config_data["level"]))
                return config_data
            except json.JSONDecodeError as error:
                print(error)


class ConfigValidator:
    def __init__(self, config_data: dict):
        self.config_data = config_data

    def validate(self):
        for key, value in self.config_data.items():
            if key == "level":
                for item in self.config_data[key]:
                    if item < 0:
                        print(f"you enter value < 0 {key} this value {item}")
