from bfs_solver import BFSSolver

class Ghost:

    def __init__(self, start_position, color):
        self.start_position = start_position
        self.position = start_position
        self.color = color
        self.direction = "DOWN"
        self.cell_size = 45

        self.pixel_position = [
            start_position[1] * self.cell_size,
            start_position[0] * self.cell_size
        ]

        self.speed = 5

        self.bfs = BFSSolver()

    def move(self, new_position, maze, ghosts):
        if not maze.is_valid_position(new_position):
            return

        for ghost in ghosts:
            if ghost != self:
                if ghost.position == new_position:
                    print("Blocked: ghost already there")
                    return

        old_row, old_col = self.position
        new_row, new_col = new_position

        if old_row > new_row:
            self.direction = "UP"
        elif old_row < new_row:
            self.direction = "DOWN"
        elif new_col < old_col:
            self.direction = "LEFT"
        elif new_col > old_col:
            self.direction = "RIGHT"

        self.position = new_position

    def update_pixel_position(self):

        target_x = self.position[1] * self.cell_size
        target_y = self.position[0] * self.cell_size


        if self.pixel_position[0] < target_x:
            self.pixel_position[0] += self.speed

        elif self.pixel_position[0] > target_x:
            self.pixel_position[0] -= self.speed


        if self.pixel_position[1] < target_y:
            self.pixel_position[1] += self.speed

        elif self.pixel_position[1] > target_y:
            self.pixel_position[1] -= self.speed

    def chase(self, maze, player_position, ghosts):

        path = self.bfs.find_path(
            maze,
            self.position,
            player_position
        )

        if len(path) > 1:
            self.move(path[1], maze, ghosts)

    def reset_position(self):
        self.position = self.start_position

        