from typing import List, Tuple

from constants import Position
from ghost import Ghost
from maze_manager import MazeManager
from reverse_bfs import ReverseBFSSolver

Candidate = Tuple[Position, int]


class GhostManager:
    """Coordinates escape targets for every FRIGHTENED ghost at once."""

    def __init__(self) -> None:
        """Create the reverse-BFS solver used to rank escape candidates."""
        self.reverse_bfs = ReverseBFSSolver()

    def update_frightened_targets(
        self,
        ghosts: List[Ghost],
        maze: MazeManager,
        player_position: Position,
    ) -> None:
        """Give each ghost a distinct, far-from-the-player escape target.

        Farther cells are preferred, and targets are spread apart so
        ghosts do not all flee toward the same corner. If the maze has
        no reachable cells at all, ghosts are simply left without a
        target for this tick rather than crashing.

        Args:
            ghosts: The ghosts to assign escape targets to (normally
                only the currently FRIGHTENED ones).
            maze: The maze to compute distances across.
            player_position: The player's current (row, col).
        """
        distances = self.reverse_bfs.calculate_distances(maze, player_position)

        if not distances:
            return

        candidates: List[Candidate] = sorted(
            distances.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        selected_targets: List[Position] = []

        for ghost in ghosts:
            target = self._pick_spread_target(candidates, selected_targets)
            ghost.escape_target = target
            selected_targets.append(target)

    def _pick_spread_target(
        self,
        candidates: List[Candidate],
        selected_targets: List[Position],
    ) -> Position:
        """Pick the candidate that is farthest from every selected target.

        The first ghost simply gets the cell farthest from the player.
        Every ghost after that gets whichever remaining candidate
        maximises its distance to the *nearest* already-selected
        target, so ghosts spread out to distinct corners instead of
        collapsing onto the same escape point. Ties are broken toward
        the candidate farther from the player, since candidates are
        given farthest-first.

        Args:
            candidates: (position, distance-to-player) pairs, sorted
                from farthest to nearest.
            selected_targets: Targets already handed out this call.

        Returns:
            The chosen position. Only repeats an already-selected
            target if there are truly no other reachable cells left.
        """
        if not selected_targets:
            return candidates[0][0]

        best_position = candidates[0][0]
        best_score = -1

        for position, _distance in candidates:
            if position in selected_targets:
                continue

            score = min(
                self._manhattan_distance(position, target)
                for target in selected_targets
            )

            if score > best_score:
                best_score = score
                best_position = position

        return best_position

    def _manhattan_distance(self, pos1: Position, pos2: Position) -> int:
        """Return the Manhattan (grid) distance between two cells."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])