from bfs_solver import BFSSolver
from direction import Direction

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
        self.target_position = start_position
        self.moving = False

        self.speed = 2

        self.bfs = BFSSolver()
        self.state = "NORMAL"

    def move(self, new_position, maze, ghosts):
        if not maze.is_valid_position(new_position):
            return

        for ghost in ghosts:
            if ghost != self:
                if ghost.target_position == new_position:
                    print("Blocked: ghost already there")
                    return

                if (
                    ghost.position == new_position
                    and ghost.target_position == self.position
                ):
                    print("Blocked: ghost swap")
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

        self.target_position = new_position
        self.moving = True

    def update_pixel_position(self):

        target_x = self.target_position[1] * 45
        target_y = self.target_position[0] * 45


        dx = target_x - self.pixel_position[0]
        dy = target_y - self.pixel_position[1]


        if abs(dx) <= self.speed:
            self.pixel_position[0] = target_x
        else:
            self.pixel_position[0] += self.speed if dx > 0 else -self.speed


        if abs(dy) <= self.speed:
            self.pixel_position[1] = target_y
        else:
            self.pixel_position[1] += self.speed if dy > 0 else -self.speed


        if (
            self.pixel_position[0] == target_x
            and self.pixel_position[1] == target_y
        ):
            self.position = self.target_position
            self.moving = False

    def chase(self, maze, player_position, ghosts):

        if self.state == "FRIGHTENED":

            self.run_away(
                maze,
                player_position,
                ghosts
            )

            return


        path = self.bfs.find_path(
            maze,
            self.position,
            player_position
        )


        if len(path) > 1:

            self.move(
                path[1],
                maze,
                ghosts
            )

    def reset_position(self):

        self.position = self.start_position

        self.target_position = self.start_position

        self.pixel_position = [
            self.start_position[1] * self.cell_size,
            self.start_position[0] * self.cell_size
        ]

        self.direction = "DOWN"

        self.moving = False

  

    def become_frightened(self):
    
        self.state = "FRIGHTENED"
        print("Ghost frightened")
    
    
    
    def become_normal(self):
        
        self.state = "NORMAL"

    def run_away(self, maze, player_position, ghosts):

        row, col = self.position


        moves = [
            ((row - 1, col), Direction.UP),
            ((row + 1, col), Direction.DOWN),
            ((row, col - 1), Direction.LEFT),
            ((row, col + 1), Direction.RIGHT)
        ]


        best_position = self.position
        max_distance = -1


        for position, direction in moves:

            if not maze.is_valid_position(
                self.position,
                direction
            ):
                continue


            distance = (
                abs(position[0] - player_position[0])
                +
                abs(position[1] - player_position[1])
            )


            if distance > max_distance:

                max_distance = distance
                best_position = position



        self.move(
            best_position,
            maze,
            ghosts
        )

    def get_pixel_cell(self):

        col = round(
            self.pixel_position[0] / self.cell_size
        )

        row = round(
            self.pixel_position[1] / self.cell_size
        )

        return (row, col)