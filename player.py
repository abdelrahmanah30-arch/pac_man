from enum import Enum

class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

class Player:
    def __init__(self, start_position, lives):
        self.start_position = start_position
        self.position = start_position
        self.lives = lives
        self.direction = None

    def change_direction(self, direction):
        self.direction = direction

    def move(self, maze):
        if self.direction is None:
            return

        row, col = self.position

        if self.direction == Direction.RIGHT:
            new_position = (row, col + 1)
        elif self.direction == Direction.LEFT:
            new_position = (row, col - 1)
        elif self.direction == Direction.UP:
            new_position = (row - 1, col)
        elif self.direction == Direction.DOWN:
            new_position = (row + 1, col)

        if maze.is_valid_position(new_position):
            self.position = new_position

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1
            self.reset_position()

    def reset_position(self):
        self.position = self.start_position

    def is_alive(self):
        return self.lives > 0