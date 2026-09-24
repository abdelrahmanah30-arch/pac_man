from pacgum import PacgumType


class GumManager:

    def __init__(self, maze, player_position, ghosts):

        self.gums = {}

        self.player_position = player_position

        self.ghost_positions = [
            ghost.position
            for ghost in ghosts
        ]

        self.create_gums(maze)



    def create_gums(self, maze):

        corner_candidates = [

            # top left
            [
                (1, 1),
                (1, 2),
                (2, 1),
                (2, 2)
            ],


            # top right
            [
                (1, maze.width - 2),
                (1, maze.width - 3),
                (2, maze.width - 2),
                (2, maze.width - 3)
            ],


            # bottom left
            [
                (maze.height - 2, 1),
                (maze.height - 3, 1),
                (maze.height - 2, 2),
                (maze.height - 3, 2)
            ],


            # bottom right
            [
                (maze.height - 2, maze.width - 2),
                (maze.height - 3, maze.width - 2),
                (maze.height - 2, maze.width - 3),
                (maze.height - 3, maze.width - 3)
            ]

        ]


        super_positions = []


        for corner in corner_candidates:

            for position in corner:

                if (
                    maze.is_valid_position(position)
                    and maze.get_open_neighbors(position) > 0
                    and position != self.player_position
                    and position not in self.ghost_positions
                ):

                    super_positions.append(position)

                    break



        for row in range(maze.height):

            for col in range(maze.width):

                position = (row, col)



                # لا Gum عند اللاعب

                if position == self.player_position:

                    continue



                # لا Gum عند الأشباح

                if position in self.ghost_positions:

                    continue



                # مكان صالح وله طريق

                if (
                    maze.is_valid_position(position)
                    and maze.get_open_neighbors(position) > 0
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

            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1)

        ]


        for neighbor in neighbors:

            if maze.is_valid_position(neighbor):

                return True


        return False