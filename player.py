from direction import Direction

class Player:
    def __init__(self, start_position, lives):
        self.start_position = start_position
        self.position = start_position
        self.lives = lives
        self.direction = None

        self.move_timer = 0
        self.move_delay = 8

    def change_direction(self, direction):
        self.direction = direction

    def move(self, maze):

        if self.direction is None:
            return
    
    
        row, col = self.position

        self.move_timer += 1
        if self.move_timer < self.move_delay:
            return

        self.move_timer = 0

        if self.direction is None:
            return
    
    
        if self.direction == Direction.RIGHT:
            new_position = (row, col + 1)
    
        elif self.direction == Direction.LEFT:
            new_position = (row, col - 1)
    
        elif self.direction == Direction.UP:
            new_position = (row - 1, col)
    
        elif self.direction == Direction.DOWN:
            new_position = (row + 1, col)
    
        else:
            return
    
    
    
        if maze.is_valid_position(
            self.position,
            self.direction
        ):
            self.position = new_position

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
            self.reset_position()

    def reset_position(self):
        self.position = self.start_position

    def is_alive(self):
        return self.lives > 0