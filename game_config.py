class GameConfig:
    def __init__(self, valid):
        self.width = valid.config_data["width"]
        self.height = valid.config_data["height"]
        self.seed = valid.config_data["seed"]
        self.lives = valid.config_data["lives"]
        self.levels = valid.config_level
        self.pacgum = valid.config_data["pacgum"]
        self.points_per_pacgum = valid.config_data["points_per_pacgum"]
        self.points_per_super_pacgum = valid.config_data["points_per_super_pacgum"]
        self.points_per_ghost = valid.config_data["points_per_ghost"]
        self.level_max_time = valid.config_data["level_max_time"]
        self.highscore_filename = valid.config_data["highscore_filename"]

    def General(self):
        ...