from collections import deque
from typing import Deque, Dict

from constants import Position
from maze_manager import MazeManager


class ReverseBFSSolver:
    """Computes BFS distances from one cell to every reachable cell."""

    def calculate_distances(
        self,
        maze: MazeManager,
        start: Position,
    ) -> Dict[Position, int]:
        """Return every reachable cell's distance from start.

        Args:
            maze: The maze to search in.
            start: The (row, col) cell to measure distances from.

        Returns:
            A mapping of every reachable position to its distance
            from start, in steps. Always includes start itself (at
            distance 0).
        """
        queue: Deque[Position] = deque([start])
        distances: Dict[Position, int] = {start: 0}

        while queue:
            current = queue.popleft()

            for neighbor in maze.get_neighbor_cells(current):
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)

        return distances
