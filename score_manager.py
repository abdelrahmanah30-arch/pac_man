from pacgum import PacgumType

class ScoreManager:

    def __init__(self, config):
        self.score = 0
        self.pacgum_points = config.points_per_pacgum
        self.super_pacgum_points = config.points_per_super_pacgum


    def add_pacgum_score(self, pacgum_type):

        if pacgum_type == PacgumType.NORMAL:
            self.score += self.pacgum_points

        elif pacgum_type == PacgumType.SUPER:
            self.score += self.super_pacgum_points


    def get_score(self):
        return self.score