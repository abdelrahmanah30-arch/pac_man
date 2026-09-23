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
    
        sizes = {
            1: (15, 15),
            2: (15, 15),
            3: (17, 15),
            4: (17, 15),
            5: (19, 15),
            6: (19, 17),
            7: (21, 17),
            8: (21, 19),
            9: (23, 19),
            10: (26, 19)
        }
    
        return sizes[self.level]


    def get_seed(self):

        # random mode

        if self.base_seed == -1:

            return random.randint(
                0,
                999999
            )
        


        # fixed seed mode

        return self.base_seed