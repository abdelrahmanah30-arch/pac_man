from game_config import GameConfig
from pacgum import PacgumType
 
 
class ScoreManager:
    """Accumulates points for gums and ghosts eaten, per the config."""
 
    def __init__(self, config: GameConfig) -> None:
        """Read the point values to award from the game configuration.
 
        Args:
            config: The validated game configuration.
        """
        self.score = 0
        self.pacgum_points = config.points_per_pacgum
        self.super_pacgum_points = config.points_per_super_pacgum
        self.ghost_points = config.points_per_ghost
 
    def add_pacgum_score(self, pacgum_type: PacgumType) -> None:
        """Award points for eating a gum of the given type."""
        if pacgum_type == PacgumType.NORMAL:
            self.score += self.pacgum_points
        elif pacgum_type == PacgumType.SUPER:
            self.score += self.super_pacgum_points
 
    def add_ghost_score(self) -> None:
        """Award points for eating a frightened ghost."""
        self.score += self.ghost_points
 
    def get_score(self) -> int:
        """Return the current score."""
        return self.score
 
    def reset(self) -> None:
        """Reset the score to 0, e.g. when starting a new game."""
        self.score = 0
 