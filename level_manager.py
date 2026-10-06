import random
from typing import Dict, Tuple

from game_config import GameConfig

MAX_LEVEL = 10
RANDOM_SEED_MAX = 999_999

DEFAULT_MAZE_SIZES: Dict[int, Tuple[int, int]] = {
    1: (15, 15),
    2: (15, 15),
    3: (17, 15),
    4: (17, 15),
    5: (19, 15),
    6: (19, 17),
    7: (21, 17),
    8: (21, 19),
    9: (23, 19),
    10: (26, 19),
}


class LevelManager:
    """Tracks progression through the game's 10 levels."""

    def __init__(self, config: GameConfig) -> None:
        """Start at level 1 with the given configuration.

        Args:
            config: The validated game configuration.
        """
        self.config = config
        self.level = 1

    def get_level(self) -> int:
        """Return the current 1-based level number."""
        return self.level

    def next_level(self) -> bool:
        """Advance to the next level, if any remain.

        Returns:
            True if there was a next level to move to, False if the
            player was already on the final level.
        """
        if self.level >= MAX_LEVEL:
            return False

        self.level += 1
        return True

    def get_maze_size(self) -> Tuple[int, int]:
        """Return this level's (width, height).

        Uses the configuration's per-level override when one is
        valid, otherwise falls back to the game's built-in default
        size for the current level.
        """
        override = self.config.get_level_size_override(self.level)

        if override is not None:
            return override

        return DEFAULT_MAZE_SIZES.get(
            self.level, DEFAULT_MAZE_SIZES[MAX_LEVEL]
        )

    def get_seed(self) -> int:
        """Return the seed to generate this level's maze with.

        Level 1 uses the configured seed, unless it is 0 or negative:
        the maze generator itself treats a non-positive seed as "pick
        a random one", so a positive seed is generated here instead
        so the game can still record/display which seed was used.
        Every level after the first is always randomly seeded, as the
        subject requires.
        """
        if self.level == 1 and self.config.seed > 0:
            return self.config.seed

        return random.randint(1, RANDOM_SEED_MAX)
