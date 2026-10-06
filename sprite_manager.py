from typing import Dict, Optional

import pygame

from direction import Direction
from ghost import GhostState

GHOST_COLORS = ["blue", "green", "orange", "purple"]
DIRECTIONS = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

FRIGHTENED_TINT_COLOR = (100, 150, 255)


class SpriteManager:
    """Loads every sprite once and hands back the right one on request."""

    def __init__(self, cell_size: int) -> None:
        """Prepare empty sprite tables sized for cell_size pixels.

        Args:
            cell_size: The pixel size every sprite is scaled to.
        """
        self.cell_size = cell_size

        self.ghosts: Dict[str, Dict[str, pygame.Surface]] = {}
        self.frightened_ghosts: Dict[str, Dict[str, pygame.Surface]] = {}
        self.ghost_eyes: Dict[str, pygame.Surface] = {}

        self.player_open: Optional[pygame.Surface] = None
        self.player_close: Optional[pygame.Surface] = None

    def load_sprites(self) -> None:
        """Load every sprite image from disk and scale it to cell_size."""
        self.player_close = self._load_scaled("assets/player/close.png")
        self.player_open = self._load_scaled("assets/player/pacman.png")

        for direction in DIRECTIONS:
            image = self._load_scaled(
                f"assets/ghosts/eye_{direction.name.lower()}.png"
            )
            self.ghost_eyes[direction.name] = image

        for color in GHOST_COLORS:
            self.ghosts[color] = {}
            self.frightened_ghosts[color] = {}

            for direction in DIRECTIONS:
                image = self._load_scaled(
                    f"assets/ghosts/{color}_{direction.name.lower()}.png"
                )
                self.ghosts[color][direction.name] = image

                frightened = image.copy()
                frightened.fill(
                    FRIGHTENED_TINT_COLOR,
                    special_flags=pygame.BLEND_RGB_MULT,
                )
                self.frightened_ghosts[color][direction.name] = frightened

    def _load_scaled(self, path: str) -> pygame.Surface:
        """Load an image from path and scale it to a cell_size square."""
        image = pygame.image.load(path)
        return pygame.transform.scale(image, (self.cell_size, self.cell_size))

    def get_player(
        self,
        direction: Optional[Direction] = None,
        mouth_open: bool = False,
    ) -> pygame.Surface:
        """Return the player sprite, rotated to face direction.

        Args:
            direction: Which way the player is facing. None keeps the
                sprite's default (rightward) orientation.
            mouth_open: Whether to use the mouth-open animation frame.
        """
        image = self.player_open if mouth_open else self.player_close

        if direction == Direction.LEFT:
            return pygame.transform.rotate(image, 180)
        if direction == Direction.UP:
            return pygame.transform.rotate(image, 90)
        if direction == Direction.DOWN:
            return pygame.transform.rotate(image, -90)

        return image

    def get_ghost(
        self,
        color: str,
        direction: Direction,
        state: GhostState = GhostState.NORMAL,
    ) -> Optional[pygame.Surface]:
        """Return the correct ghost sprite for its colour, facing and state.

        Args:
            color: The ghost's sprite colour key (e.g. "blue").
            direction: Which way the ghost is facing.
            state: The ghost's current behavioural state.

        Returns:
            The matching sprite, or None if no sprite matches (e.g. an
            unknown colour), so the caller can safely skip drawing it.
        """
        if state == GhostState.EATEN:
            return self.ghost_eyes.get(direction.name)

        if state == GhostState.FRIGHTENED:
            return self.frightened_ghosts.get(color, {}).get(direction.name)

        return self.ghosts.get(color, {}).get(direction.name)
