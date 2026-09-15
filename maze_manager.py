import random


class MazeManager:

    WALL = "#"
    PATH = "_"
    GHOST = "G"


    def __init__(self, width, height, seed):

        if width < 21 or height < 21:
            raise ValueError(
                "Maze size must be at least 21x21 for 42 design"
            )

        self.width = width
        self.height = height
        self.seed = seed

        random.seed(seed)

        self.maze = []

        self.generate()



    def generate(self):

        # create empty maze

        self.maze = [
            [self.PATH for _ in range(self.width)]
            for _ in range(self.height)
        ]


        self.create_border()


        # Fixed 42 in the center

        self.create_42()


        # Ghost house

        self.create_ghost_house()


        # random walls outside the 42

        self.create_random_walls()



    def create_border(self):

        for col in range(self.width):

            self.maze[0][col] = self.WALL
            self.maze[self.height - 1][col] = self.WALL


        for row in range(self.height):

            self.maze[row][0] = self.WALL
            self.maze[row][self.width - 1] = self.WALL



    def create_42(self):

        """
        Draw 42 using walls
        Always in the center
        """

        center_row = self.height // 2
        center_col = self.width // 2


        # Scale depending on maze size

        size = min(
            self.width,
            self.height
        ) // 8


        if size < 3:
            size = 3



        four = []


        # left vertical

        for i in range(-size, size):

            four.append(
                (
                    center_row + i,
                    center_col - size
                )
            )


        # middle bar

        for i in range(-size, 1):

            four.append(
                (
                    center_row,
                    center_col - size + i
                )
            )


        # right vertical of 4

        for i in range(0, size):

            four.append(
                (
                    center_row + i,
                    center_col
                )
            )



        two = []


        # top horizontal

        for i in range(-size, size + 1):

            two.append(
                (
                    center_row - size,
                    center_col + i + 3
                )
            )


        # right side

        for i in range(-size, 1):

            two.append(
                (
                    center_row + i,
                    center_col + size + 3
                )
            )


        # diagonal

        for i in range(size + 1):

            two.append(
                (
                    center_row + i,
                    center_col + size + 3 - i
                )
            )


        # bottom line

        for i in range(-size, size + 1):

            two.append(
                (
                    center_row + size,
                    center_col + i + 3
                )
            )



        for row, col in four + two:

            if self.is_inside(row, col):

                self.maze[row][col] = self.WALL




    def create_ghost_house(self):

        row = self.height // 2 + 5
        col = self.width // 2


        for r in range(row - 1, row + 2):

            for c in range(col - 4, col + 5):

                if self.is_inside(r, c):

                    self.maze[r][c] = self.GHOST




    def create_random_walls(self):

        random.seed(self.seed)


        center_row = self.height // 2
        center_col = self.width // 2


        for _ in range(
            (self.width * self.height) // 15
        ):

            row = random.randint(
                2,
                self.height - 3
            )

            col = random.randint(
                2,
                self.width - 3
            )


            # don't destroy center

            if (
                abs(row - center_row) < 6
                and
                abs(col - center_col) < 8
            ):
                continue


            self.maze[row][col] = self.WALL




    def is_inside(self, row, col):

        return (
            0 <= row < self.height
            and
            0 <= col < self.width
        )



    def is_valid_position(self, position):

        row, col = position


        if not self.is_inside(row, col):

            return False


        if self.maze[row][col] == self.WALL:

            return False


        return True



    def get_neighbors(self, position):

        row, col = position


        directions = [

            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1)

        ]


        neighbors = []


        for dr, dc in directions:

            cell = (
                row + dr,
                col + dc
            )


            if self.is_valid_position(cell):

                neighbors.append(cell)


        return neighbors



    def get_empty_cells(self):

        cells = []


        for row in range(self.height):

            for col in range(self.width):

                if self.maze[row][col] == self.PATH:

                    cells.append(
                        (row, col)
                    )


        return cells



    def display(self):

        for row in self.maze:

            print(
                "".join(row)
            )