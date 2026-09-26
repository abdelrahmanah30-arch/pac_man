from typing import List, Optional
 
from constants import CELL_SIZE, Position
from direction import Direction
from maze_manager import MazeManager
 
MOVE_DELAY_TICKS = 8
MOUTH_OPEN_TICKS = 8
PLAYER_SPEED = 5
 
 
class Player:
    """The player-controlled Pac-Man character."""
 
    def __init__(self, start_position: Position, lives: int) -> None:
        """Spawn the player at start_position with the given lives.
 
        Args:
            start_position: The (row, col) spawn cell.
            lives: How many lives the player starts with.
        """
        self.start_position = start_position
        self.position = start_position
        self.lives = lives
 
        self.direction: Optional[Direction] = None
 
        self.mouth_open = False
        self.mouth_timer = 0
 
        self.pixel_position: List[int] = [
            start_position[1] * CELL_SIZE,
            start_position[0] * CELL_SIZE,
        ]
 
        self.speed = PLAYER_SPEED
        self.move_timer = 0
        self.move_delay = MOVE_DELAY_TICKS
 
    def change_direction(self, direction: Direction) -> None:
        """Set the direction the player will try to move in next."""
        self.direction = direction
 
    def move(self, maze: MazeManager) -> None:
        """Advance one grid cell in the current direction, if possible.
 
        Movement is throttled to once every move_delay ticks, so the
        player advances one cell at a fixed pace rather than every
        frame.
 
        Args:
            maze: The maze to check for walls against.
        """
        if self.direction is None:
            return
 
        self.move_timer += 1
 
        if self.move_timer < self.move_delay:
            return
 
        self.move_timer = 0
 
        if not maze.is_valid_position(self.position, self.direction):
            return
 
        row, col = self.position
 
        if self.direction == Direction.RIGHT:
            self.position = (row, col + 1)
        elif self.direction == Direction.LEFT:
            self.position = (row, col - 1)
        elif self.direction == Direction.UP:
            self.position = (row - 1, col)
        elif self.direction == Direction.DOWN:
            self.position = (row + 1, col)
 
    def update_pixel_position(self) -> None:
        """Step the on-screen position toward the grid position by speed.
 
        Snaps exactly onto the target once within one step of it,
        rather than overshooting back and forth around it forever.
        """
        target_x = self.position[1] * CELL_SIZE
        target_y = self.position[0] * CELL_SIZE
 
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
 
    def lose_life(self) -> None:
        """Lose one life and respawn at the start, if any lives remain."""
        if self.lives > 0:
            self.lives -= 1
            self.reset_position()
 
    def reset_position(self) -> None:
        """Snap the player back to its spawn cell."""
        self.position = self.start_position
 
        self.pixel_position = [
            self.start_position[1] * CELL_SIZE,
            self.start_position[0] * CELL_SIZE,
        ]
 
        self.direction = None
 
    def is_alive(self) -> bool:
        """Return True if the player still has lives remaining."""
        return self.lives > 0
 
    def update_mouth(self) -> None:
        """Count down the mouth-open animation timer."""
        if self.mouth_timer > 0:
            self.mouth_timer -= 1
        else:
            self.mouth_open = False
 
    def open_mouth(self) -> None:
        """Trigger the mouth-open animation (e.g. after eating a gum)."""
        self.mouth_open = True
        self.mouth_timer = MOUTH_OPEN_TICKS
 
    def get_pixel_cell(self) -> Position:
        """Return the maze cell the player's sprite currently occupies."""
        col = round(self.pixel_position[0] / CELL_SIZE)
        row = round(self.pixel_position[1] / CELL_SIZE)
        return row, col
 
