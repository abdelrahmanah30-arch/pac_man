from pacgum import PacgumType


class GumManager:

    def __init__(self, maze):

        self.gums = {}

        self.create_gums(maze)


    def create_gums(self, maze):

        for row in range(maze.height):

            for col in range(maze.width):

                if (
                    maze.is_valid_position((row,col))
                    and maze.get_open_neighbors((row,col))
                ):

                    self.gums[(row,col)] = PacgumType.NORMAL


    def eat_gum(self, position):

        if position in self.gums:

            gum_type = self.gums[position]

            del self.gums[position]

            return gum_type


        return None

    def remaining(self):

        return len(self.gums)

    def has_exit(self, maze, position):

        row, col = position

        neighbors = [
            (row - 1, col),  # up
            (row + 1, col),  # down
            (row, col - 1),  # left
            (row, col + 1)   # right
        ]

        for neighbor in neighbors:

            if maze.is_valid_position(neighbor):

                return True


        return False