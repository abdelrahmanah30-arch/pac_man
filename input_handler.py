from typing import Optional
 
import pygame
 
from direction import Direction
 
_DIRECTION_KEYS = {
    pygame.K_UP: Direction.UP,
    pygame.K_w: Direction.UP,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_s: Direction.DOWN,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_a: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT,
    pygame.K_d: Direction.RIGHT,
}
 
 
class InputHandler:
    """Reads raw pygame events and turns them into simple game inputs."""
 
    def __init__(self) -> None:
        """Start with no direction and no pending one-shot inputs."""
        self.direction: Optional[Direction] = None
        self._next_level_pressed = False
        self._pause_pressed = False
        self._confirm_pressed = False
 
    def handle_input(self) -> bool:
        """Process every pygame event queued up since the last call.
 
        Returns:
            False if the window's close button was clicked (the game
            should stop), True otherwise.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
 
            if event.type != pygame.KEYDOWN:
                continue
 
            if event.key == pygame.K_F1:
                self._next_level_pressed = True
            elif event.key == pygame.K_ESCAPE:
                self._pause_pressed = True
            elif event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self._confirm_pressed = True
            elif event.key in _DIRECTION_KEYS:
                self.direction = _DIRECTION_KEYS[event.key]
 
        return True
 
    def get_direction(self) -> Optional[Direction]:
        """Return the last movement direction pressed (arrows or WASD)."""
        return self.direction
 
    def get_next_level(self) -> bool:
        """Return and clear the one-shot 'skip to next level' input.
 
        Note:
            This reports the F1 key only; it is a debug-style shortcut
            and does not itself decide whether that is part of the
            final cheat mode.
        """
        if self._next_level_pressed:
            self._next_level_pressed = False
            return True
        return False
 
    def get_pause(self) -> bool:
        """Return and clear the one-shot 'toggle pause' input (Escape)."""
        if self._pause_pressed:
            self._pause_pressed = False
            return True
        return False
 
    def get_confirm(self) -> bool:
        """Return and clear the one-shot 'confirm/start' input.
 
        Triggered by Space or Enter. Generic on purpose: whoever
        builds the Main Menu / Game Over screens can reuse this same
        signal for "start game", "submit name", etc.
        """
        if self._confirm_pressed:
            self._confirm_pressed = False
            return True
        return False
 
