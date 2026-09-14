from bfs_solver import BFSSolver

class Ghost:

    def __init__(self, start_position, color):
        self.start_position = start_position
        self.position = start_position
        self.color = color
        self.bfs = BFSSolver()

    def move(self, new_position, maze):
        if maze.is_valid_position(new_position):
            self.position = new_position

    def chase(self, maze, player_position):

        path = self.bfs.find_path(
            maze,
            self.position,
            player_position
        )

        if len(path) > 1:
            self.move(path[1], maze)

    def reset_position(self):
        self.position = self.start_position

        