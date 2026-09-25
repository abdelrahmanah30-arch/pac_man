from __future__ import annotations

from enum import Enum
from typing import List, Optional

from bfs_solver import BFSSolver
from constants import CELL_SIZE, Position
from direction import Direction
from maze_manager import MazeManager

RESPAWN_TICKS = 60
GHOST_SPEED = 2


class GhostState(Enum):
    """The behavioural state a ghost can be in."""

    NORMAL = "NORMAL"
    FRIGHTENED = "FRIGHTENED"
    EATEN = "EATEN"
    WAITING = "WAITING"


class Ghost:
    """An autonomous ghost that chases, flees from, or waits for the player."""

    def __init__(self, start_position: Position, color: str) -> None:
        """Create a ghost at its spawn corner.

        Args:
            start_position: The (row, col) spawn/home cell.
            color: The ghost's sprite colour key (e.g. "blue").
        """
        self.start_position = start_position
        self.position = start_position
        self.color = color

        self.direction: Direction = Direction.DOWN

        self.pixel_position: List[int] = [
            start_position[1] * CELL_SIZE,
            start_position[0] * CELL_SIZE,
        ]

        self.target_position: Position = start_position
        self.previous_position: Optional[Position] = None

        # Assigned externally by GhostManager while FRIGHTENED.
        self.escape_target: Optional[Position] = None

        self.moving = False
        self.speed = GHOST_SPEED
        self.respawn_timer = 0

        self.bfs = BFSSolver()

        self.state: GhostState = GhostState.NORMAL
        self.eaten = False

    def move(
        self,
        new_position: Position,
        maze: MazeManager,
        ghosts: List[Ghost],
    ) -> None:
        """Start moving toward new_position if it is free to enter.

        Args:
            new_position: The adjacent cell to move into.
            maze: The maze, used for a bounds sanity check.
            ghosts: Every ghost in play, used to avoid two ghosts
                swapping into each other's cell on the same tick.
        """
        if not maze.is_valid_position(new_position):
            return

        for ghost in ghosts:
            if ghost is self:
                continue

            if ghost.target_position == new_position:
                return

            if (
                ghost.position == new_position
                and ghost.target_position == self.position
            ):
                return

        old_row, old_col = self.position
        new_row, new_col = new_position

        if old_row > new_row:
            self.direction = Direction.UP
        elif old_row < new_row:
            self.direction = Direction.DOWN
        elif new_col < old_col:
            self.direction = Direction.LEFT
        elif new_col > old_col:
            self.direction = Direction.RIGHT

        self.target_position = new_position
        self.moving = True

    def update(self) -> None:
        """Advance the respawn countdown while WAITING, then go NORMAL."""
        if self.state == GhostState.WAITING:
            self.respawn_timer -= 1

            if self.respawn_timer <= 0:
                self.become_normal()

    def update_pixel_position(self) -> None:
        """Step the on-screen position toward target_position by speed."""
        target_x = self.target_position[1] * CELL_SIZE
        target_y = self.target_position[0] * CELL_SIZE

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
            self.previous_position = self.position
            self.position = self.target_position
            self.moving = False

            if self.position == self.escape_target:
                self.escape_target = None

    def chase(
        self,
        maze: MazeManager,
        player_position: Position,
        ghosts: List[Ghost],
    ) -> None:
        """Pick the ghost's next move for this tick, based on its state.

        Args:
            maze: The maze to path-find through.
            player_position: The player's current (row, col).
            ghosts: Every ghost in play, for collision avoidance.
        """
        if self.state == GhostState.EATEN:
            self.return_home(maze, ghosts)
            return

        if self.state == GhostState.WAITING:
            return

        if self.state == GhostState.FRIGHTENED:
            if self.escape_target is None:
                return

            path = self.bfs.find_path(maze, self.position, self.escape_target)

            if len(path) > 1:
                self.move(path[1], maze, ghosts)
            return

        # NORMAL: chase the player directly.
        path = self.bfs.find_path(maze, self.position, player_position)

        if len(path) > 1:
            self.move(path[1], maze, ghosts)

    def return_home(self, maze: MazeManager, ghosts: List[Ghost]) -> None:
        """Path back to the spawn corner, then start the respawn wait.

        Args:
            maze: The maze to path-find through.
            ghosts: Every ghost in play, for collision avoidance.
        """
        if self.position == self.start_position:
            self.moving = False
            self.respawn_timer = RESPAWN_TICKS
            self.state = GhostState.WAITING
            return

        path = self.bfs.find_path(maze, self.position, self.start_position)

        if len(path) > 1:
            self.move(path[1], maze, ghosts)

    def become_frightened(self) -> None:
        """Switch to FRIGHTENED: the player can now eat this ghost."""
        self.state = GhostState.FRIGHTENED
        self.escape_target = None

    def become_eaten(self) -> None:
        """Switch to EATEN: the ghost heads back to its spawn corner."""
        self.state = GhostState.EATEN
        self.eaten = True
        self.escape_target = None
        self.moving = False

    def become_normal(self) -> None:
        """Switch to NORMAL: the ghost resumes chasing the player."""
        self.state = GhostState.NORMAL
        self.eaten = False
        self.escape_target = None

    def reset_position(self) -> None:
        """Snap the ghost back to its spawn cell (its state is untouched)."""
        self.position = self.start_position
        self.target_position = self.start_position
        self.escape_target = None

        self.pixel_position = [
            self.start_position[1] * CELL_SIZE,
            self.start_position[0] * CELL_SIZE,
        ]

        self.direction = Direction.DOWN
        self.moving = False

    def get_pixel_cell(self) -> Position:
        """Return the maze cell the ghost's sprite currently occupies."""
        col = round(self.pixel_position[0] / CELL_SIZE)
        row = round(self.pixel_position[1] / CELL_SIZE)
        return row, col