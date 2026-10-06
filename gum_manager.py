from typing import Dict, List, Optional, Set

from constants import Position
from ghost import Ghost
from maze_manager import MazeManager
from pacgum import PacgumType


class GumManager:
    """Owns every pacgum on the current level and how to eat them."""

    def __init__(
        self,
        maze: MazeManager,
        player_position: Position,
        ghosts: List[Ghost],
    ) -> None:
        """Populate the maze with pacgums and super-pacgums.

        Args:
            maze: The maze to place gums into.
            player_position: The player's spawn cell (left empty).
            ghosts: The ghosts on this level (their cells are left
                empty too).
        """
        self.gums: Dict[Position, PacgumType] = {}
        self.player_position = player_position
        self.ghost_positions = [ghost.position for ghost in ghosts]

        self._create_gums(maze)

    def _create_gums(self, maze: MazeManager) -> None:
        """Fill every open, unoccupied corridor cell with a pacgum."""
        super_positions = self._pick_super_positions(maze)

        for row in range(maze.height):
            for col in range(maze.width):
                position = (row, col)

                if position == self.player_position:
                    continue

                if position in self.ghost_positions:
                    continue

                if maze.get_open_neighbors(position) == 0:
                    continue

                if position in super_positions:
                    self.gums[position] = PacgumType.SUPER
                else:
                    self.gums[position] = PacgumType.NORMAL

    def _pick_super_positions(self, maze: MazeManager) -> Set[Position]:
        """Pick one super-pacgum cell in each of the 4 maze corners.

        Each corner offers a small group of candidate cells so that a
        cell already taken by the player or a ghost does not leave
        that corner without a super-pacgum.

        Args:
            maze: The maze to pick corner cells from.

        Returns:
            The set of chosen super-pacgum positions (0 to 4 cells).
        """
        corner_candidate_groups = [
            [(1, 1), (1, 2), (2, 1), (2, 2)],
            [
                (1, maze.width - 2),
                (1, maze.width - 3),
                (2, maze.width - 2),
                (2, maze.width - 3),
            ],
            [
                (maze.height - 2, 1),
                (maze.height - 3, 1),
                (maze.height - 2, 2),
                (maze.height - 3, 2),
            ],
            [
                (maze.height - 2, maze.width - 2),
                (maze.height - 3, maze.width - 2),
                (maze.height - 2, maze.width - 3),
                (maze.height - 3, maze.width - 3),
            ],
        ]

        super_positions: Set[Position] = set()

        for candidates in corner_candidate_groups:
            for position in candidates:
                if not maze.is_valid_position(position):
                    continue
                if maze.get_open_neighbors(position) == 0:
                    continue
                if position == self.player_position:
                    continue
                if position in self.ghost_positions:
                    continue

                super_positions.add(position)
                break

        return super_positions

    def eat_gum(self, position: Position) -> Optional[PacgumType]:
        """Remove and return the gum at position, if any.

        Args:
            position: The cell the player just moved onto.

        Returns:
            The type of gum that was eaten, or None if the cell was
            already empty.
        """
        return self.gums.pop(position, None)

    def remaining(self) -> int:
        """Return how many gums are still left on the maze."""
        return len(self.gums)
