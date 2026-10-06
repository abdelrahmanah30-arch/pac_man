from collections import deque
from typing import Deque, Dict, List, Tuple
from maze_manager import MazeManager
Position = Tuple[int, int]


class BFSSolver:
    """Finds the shortest path between two cells of a maze using BFS."""

    def find_path(
        self,
        maze: MazeManager,
        start: Position,
        goal: Position,
    ) -> List[Position]:
        """Return the shortest path from start to goal.

        Args:
            maze: The maze to search in.
            start: Starting (row, col) position.
            goal: Target (row, col) position.

        Returns:
            The list of positions from start to goal (inclusive), in
            order. Returns an empty list if no path exists.
        """
        queue: Deque[Position] = deque([start])
        visited: set[Position] = {start}
        parent: Dict[Position, Position] = {}

        while queue:
            current = queue.popleft()

            if current == goal:
                return self._reconstruct_path(parent, start, goal)

            for neighbor in maze.get_neighbor_cells(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = current
                    queue.append(neighbor)

        return []

    def _reconstruct_path(
        self,
        parent: Dict[Position, Position],
        start: Position,
        goal: Position,
    ) -> List[Position]:
        """Walk the parent chain from goal back to start and reverse it."""
        path = [goal]
        current = goal

        while current != start:
            current = parent[current]
            path.append(current)

        path.reverse()
        return path
