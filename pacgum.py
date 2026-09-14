from enum import Enum


class PacgumType(Enum):
    NORMAL = "NORMAL"
    SUPER = "SUPER"



class Pacgum:

    def __init__(self, position, pacgum_type):
        self.position = position
        self.type = pacgum_type
        self.collected = False


    def collect(self):
        self.collected = True


    def is_collected(self):
        return self.collected