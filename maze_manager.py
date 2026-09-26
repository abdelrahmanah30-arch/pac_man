from typing import List, Optional
 
from constants import Position
from direction import Direction
from mazegenerator.mazegenerator import MazeGenerator
 
_WALL_BIT = {
    Direction.UP: 1,
    Direction.RIGHT: 2,
    Direction.DOWN: 4,
    Direction.LEFT: 8,
}
 
 
class MazeGenerationError(Exception):
    """Raised when the assigned maze generator package fails."""
 
 
class MazeManager:
    """Generates a maze via the assigned package and answers queries on it.
 
    The maze cell format follows the assigned package's convention: a
    bit is set when that side of the cell is walled off (1 = UP,
    2 = RIGHT, 4 = DOWN, 8 = LEFT).
    """
 
    def __init__(self, width: int, height: int, seed: int) -> None:
        """Generate a new maze of the given size and seed.
 
        Args:
            width: The maze width, in cells.
            height: The maze height, in cells.
            seed: A positive seed for a reproducible maze, or any
                non-positive value for a randomly generated one.
 
        Raises:
            MazeGenerationError: If the underlying generator fails.
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.maze: List[List[int]] = self._generate()
 
    def _generate(self) -> List[List[int]]:
        """Run the assigned generator once and return its maze grid.
 
        PERFECT is explicitly set to False, as the subject requires,
        so the maze keeps loops instead of being a single-path tree -
        matching classic, chase-able Pac-Man corridors.
        """
        try:
            generator = MazeGenerator(
                size=(self.width, self.height),
                perfect=False,
                seed=self.seed,
            )
        except Exception as error:
            raise MazeGenerationError(
                f"the maze generator failed for a {self.width}x"
                f"{self.height} maze: {error}"
            ) from error
 
        return generator.maze
 
    def find_center_start(self) -> Position:
        """Return the spawnable cell closest to the maze's centre."""
        center: Position = (self.height // 2, self.width // 2)
 
        all_cells = (
            (row, col)
            for row in range(self.height)
            for col in range(self.width)
        )
        closest_first = sorted(
            all_cells,
            key=lambda position: self._manhattan_distance(position, center),
        )
 
        for position in closest_first:
            if self.can_spawn(position):
                return position
 
        return (1, 1)
 
    def can_spawn(self, position: Position) -> bool:
        """Return True if position is in bounds and has an open side."""
        if not self.is_valid_position(position):
            return False
 
        return self.get_open_neighbors(position) > 0
 
    def is_valid_position(
        self,
        position: Position,
        direction: Optional[Direction] = None,
    ) -> bool:
        """Return True if position is in bounds and, if given, that
        side of the cell is not walled off.
 
        Args:
            position: The (row, col) cell to check.
            direction: If given, also require this side to be open.
        """
        row, col = position
 
        if row < 0 or row >= self.height:
            return False
 
        if col < 0 or col >= self.width:
            return False
 
        if direction is not None:
            cell = self.maze[row][col]
            if cell & _WALL_BIT[direction]:
                return False
 
        return True
 
    def get_open_neighbors(self, position: Position) -> int:
        """Return how many of the 4 sides of position are open."""
        return sum(
            self.is_valid_position(position, direction)
            for direction in Direction
        )
 
    def get_neighbor_cells(self, position: Position) -> List[Position]:
        """Return every cell reachable from position in a single step.
 
        Used by the BFS-based solvers instead of each re-implementing
        the same wall-aware neighbor search.
 
        Args:
            position: The (row, col) cell to look around.
 
        Returns:
            The list of adjacent cells with no wall in between.
        """
        row, col = position
        candidates = [
            ((row - 1, col), Direction.UP),
            ((row + 1, col), Direction.DOWN),
            ((row, col - 1), Direction.LEFT),
            ((row, col + 1), Direction.RIGHT),
        ]
 
        return [
            cell
            for cell, direction in candidates
            if self.is_valid_position(position, direction)
        ]
 
    def find_ghost_positions(self, count: int = 4) -> List[Position]:
        """Return up to count spawnable cells, preferring the 4 corners.
 
        Args:
            count: How many ghost spawn positions to find.
 
        Returns:
            Up to count distinct spawnable positions.
        """
        corners = [
            (1, 1),
            (1, self.width - 2),
            (self.height - 2, 1),
            (self.height - 2, self.width - 2),
        ]
 
        positions = [corner for corner in corners if self.can_spawn(corner)]
 
        if len(positions) >= count:
            return positions[:count]
 
        for row in range(self.height):
            for col in range(self.width):
                position = (row, col)
 
                if position in positions:
                    continue
 
                if self.can_spawn(position):
                    positions.append(position)
 
                if len(positions) == count:
                    return positions
 
        return positions
 
    def _manhattan_distance(self, pos1: Position, pos2: Position) -> int:
        """Return the Manhattan (grid) distance between two cells."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
 
