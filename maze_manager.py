from mazegenerator.mazegenerator import MazeGenerator
from direction import Direction


class MazeManager:

    def __init__(self, width, height, seed):

        self.width = width
        self.height = height
        self.seed = seed

        self.generator = None
        self.maze = None

        self.generate()



    def generate(self):

        self.generator = MazeGenerator(
            size=(self.width, self.height),
            seed=self.seed
        )

        self.generator.generate(
            self.seed
        )

        self.maze = self.generator.maze

    def find_center_start(self):

        center_row = self.height // 2
        center_col = self.width // 2


        positions = [
            (center_row + 2, center_col),
            (center_row + 2, center_col - 1),
            (center_row + 2, center_col + 1),
            (center_row + 3, center_col),
            (center_row + 1, center_col)
        ]


        for position in positions:

            if self.is_valid_position(position):
                return position


        return (1,1)

    def is_valid_position(self, position, direction=None):

        row, col = position


        if row < 0 or row >= self.height:
            return False

        if col < 0 or col >= self.width:
            return False


        current = self.maze[row][col]


        if direction == Direction.UP:

            if current & 1:
                return False


        elif direction == Direction.RIGHT:

            if current & 2:
                return False


        elif direction == Direction.DOWN:

            if current & 4:
                return False


        elif direction == Direction.LEFT:

            if current & 8:
                return False


        return True