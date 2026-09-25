from typing import List, Optional, Tuple

from config_loader import ConfigValidator

LevelSizeOverride = Optional[Tuple[int, int]]


class GameConfig:
    """Immutable, validated view of the game's configuration.

    Built from an already-validated ConfigValidator, so every
    attribute here is guaranteed to hold a safe, correctly-typed
    value; callers never need to re-check it.
    """

    def __init__(self, validator: ConfigValidator) -> None:
        """Copy every validated setting out of a ConfigValidator.

        Args:
            validator: A ConfigValidator whose validate() method has
                already been called.
        """
        config_data = validator.config_data

        self.highscore_filename: str = config_data["highscore_filename"]
        self.lives: int = config_data["lives"]
        self.pacgum: int = config_data["pacgum"]
        self.points_per_pacgum: int = config_data["points_per_pacgum"]
        self.points_per_super_pacgum: int = config_data[
            "points_per_super_pacgum"
        ]
        self.points_per_ghost: int = config_data["points_per_ghost"]
        self.seed: int = config_data["seed"]
        self.level_max_time: int = config_data["level_max_time"]

        self.level_size_overrides: List[LevelSizeOverride] = (
            validator.config_level
        )

    def get_level_size_override(self, level_number: int) -> LevelSizeOverride:
        """Return the configured size override for a level, if any.

        Args:
            level_number: The 1-based level number.

        Returns:
            A (width, height) tuple if the configuration provides a
            valid override for that level, otherwise None - meaning
            the caller should fall back to its own default size.
        """
        index = level_number - 1

        if 0 <= index < len(self.level_size_overrides):
            return self.level_size_overrides[index]

        return None