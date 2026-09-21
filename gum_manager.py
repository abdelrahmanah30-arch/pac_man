from pacgum import PacgumType


class GumManager:

    def __init__(self, maze):

        self.gums = {}

        self.create_gums(maze)


    def create_gums(self, maze):

        super_positions = [
            (1, 1),
            (1, maze.width - 2),
            (maze.height - 2, 1),
            (maze.height - 2, maze.width - 2)
        ]


        for row in range(maze.height):

            for col in range(maze.width):

                position = (row, col)

                if (
                    maze.is_valid_position(position)
                    and maze.get_open_neighbors(position)
                ):

                    if position in super_positions:

                        self.gums[position] = PacgumType.SUPER

                    else:

                        self.gums[position] = PacgumType.NORMAL


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