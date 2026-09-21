import random


class LevelManager:

    def __init__(self, config):

        self.level = 1

        self.base_seed = config.seed


    def get_level(self):

        return self.level


    def next_level(self):

        if self.level < 10:

            self.level += 1

            return True


        return False


    def get_maze_size(self):

        size = 15 + (self.level - 1) * 2

        return min(size, 25)


    def get_seed(self):

        # random mode

        if self.base_seed == -1:

            return random.randint(
                0,
                999999
            )


        # fixed seed mode

        return self.base_seed