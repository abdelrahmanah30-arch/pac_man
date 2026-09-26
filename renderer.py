from typing import Dict, List, Optional, Tuple
 
import pygame
 
from constants import CELL_SIZE, Position
from ghost import Ghost
from high_score import HighScoreEntry
from pacgum import PacgumType
from player import Player
from sprite_manager import SpriteManager
 
TOP_BAR_HEIGHT = 90
WALL_WIDTH = 3
 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
 
NORMAL_GUM_RADIUS = 4
SUPER_GUM_RADIUS = 9
 
 
class Renderer:
    """Draws the maze, HUD, and every menu/end screen with pygame."""
 
    def __init__(self, width: int, height: int) -> None:
        """Prepare a renderer sized for a width x height maze.
 
        Args:
            width: The maze width, in cells.
            height: The maze height, in cells.
        """
        self.width = width
        self.height = height
 
        self.screen: Optional[pygame.Surface] = None
        self.screen_width = 0
        self.screen_height = 0
 
        self.font: Optional[pygame.font.Font] = None
        self.title_font: Optional[pygame.font.Font] = None
 
        self.sprite_manager = SpriteManager(CELL_SIZE)
 
    def initialize(self) -> None:
        """Set up the pygame window, fonts, and sprites."""
        pygame.init()
        self._update_screen_size()
 
        self.font = pygame.font.SysFont(None, 30)
        self.title_font = pygame.font.SysFont(None, 60)
 
        self.sprite_manager.load_sprites()
        pygame.display.set_caption("Pac-Man 42")
 
    def update_size(self, width: int, height: int) -> None:
        """Resize the window for a new level's maze dimensions."""
        self.width = width
        self.height = height
        self._update_screen_size()
 
    def _update_screen_size(self) -> None:
        """Recompute and apply the window size from width/height."""
        self.screen_height = self.height * CELL_SIZE + TOP_BAR_HEIGHT
        self.screen_width = self.width * CELL_SIZE
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
 
    def clear(self) -> None:
        """Fill the screen with the background colour."""
        self.screen.fill(BLACK)
 
    def update(self) -> None:
        """Flip the display buffer to show what was just drawn."""
        pygame.display.flip()
 
    def draw_maze(self, maze: List[List[int]]) -> None:
        """Draw every cell's floor and walls.
 
        Args:
            maze: The maze grid, as returned by MazeManager.maze.
        """
        for row, cells in enumerate(maze):
            for col, cell in enumerate(cells):
                x = col * CELL_SIZE
                y = row * CELL_SIZE + TOP_BAR_HEIGHT
 
                pygame.draw.rect(
                    self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE)
                )
 
                if cell & 1:
                    pygame.draw.line(
                        self.screen, BLUE, (x, y), (x + CELL_SIZE, y), WALL_WIDTH
                    )
                if cell & 2:
                    pygame.draw.line(
                        self.screen,
                        BLUE,
                        (x + CELL_SIZE, y),
                        (x + CELL_SIZE, y + CELL_SIZE),
                        WALL_WIDTH,
                    )
                if cell & 4:
                    pygame.draw.line(
                        self.screen,
                        BLUE,
                        (x, y + CELL_SIZE),
                        (x + CELL_SIZE, y + CELL_SIZE),
                        WALL_WIDTH,
                    )
                if cell & 8:
                    pygame.draw.line(
                        self.screen, BLUE, (x, y), (x, y + CELL_SIZE), WALL_WIDTH
                    )
 
    def draw_player(self, player: Player) -> None:
        """Draw the player sprite at its current pixel position."""
        x, y = player.pixel_position
        y += TOP_BAR_HEIGHT
 
        self.screen.blit(
            self.sprite_manager.get_player(player.direction, player.mouth_open),
            (x, y),
        )
 
    def draw_ghosts(self, ghosts: List[Ghost]) -> None:
        """Draw every ghost's sprite at its current pixel position."""
        for ghost in ghosts:
            x, y = ghost.pixel_position
            y += TOP_BAR_HEIGHT
 
            image = self.sprite_manager.get_ghost(
                ghost.color, ghost.direction, ghost.state
            )
 
            if image:
                self.screen.blit(image, (x, y))
 
    def draw_gums(self, gums: Dict[Position, PacgumType]) -> None:
        """Draw every remaining pacgum and super-pacgum."""
        for position, gum_type in gums.items():
            row, col = position
            x = col * CELL_SIZE + CELL_SIZE // 2
            y = row * CELL_SIZE + CELL_SIZE // 2 + TOP_BAR_HEIGHT
 
            radius = (
                SUPER_GUM_RADIUS
                if gum_type == PacgumType.SUPER
                else NORMAL_GUM_RADIUS
            )
 
            pygame.draw.circle(self.screen, WHITE, (x, y), radius)
 
    def draw_hud(
        self,
        score: int,
        lives: int,
        level: int,
        time_remaining: int,
    ) -> None:
        """Draw the score, level, lives, and time-remaining bar.
 
        Args:
            score: The current score.
            lives: Remaining lives.
            level: The current 1-based level number.
            time_remaining: Seconds left before the level times out.
        """
        labels = [
            (f"Score: {score}", 20),
            (f"Level: {level}", 250),
            (f"Lives: {lives}", 450),
            (f"Time: {max(time_remaining, 0)}", 650),
        ]
 
        for text, x in labels:
            surface = self.font.render(text, True, WHITE)
            self.screen.blit(surface, (x, 20))
 
    def draw_menu(self, top_scores: List[HighScoreEntry]) -> None:
        """Draw the main menu: title, start prompt, and top highscores.
 
        Note:
            This is a minimal placeholder screen. The full Main Menu
            (Start Game / View Highscores / Instructions / Exit) is a
            separate feature.
 
        Args:
            top_scores: The current top highscore entries to display.
        """
        self._draw_centered_text(
            "Pac-Man", YELLOW, self.title_font, y_offset=-140
        )
        self._draw_centered_text(
            "Push SPACE to play", WHITE, self.font, y_offset=-60
        )
        self._draw_centered_text("highscores:", WHITE, self.font, y_offset=0)
 
        for index, entry in enumerate(top_scores):
            line = f"{index + 1}. {entry.name} - {entry.score} pts"
            self._draw_centered_text(
                line, WHITE, self.font, y_offset=30 + index * 26
            )
 
    def draw_pause(self) -> None:
        """Draw a translucent overlay with a 'PAUSED' label."""
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(160)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
 
        self._draw_centered_text("PAUSED", WHITE, self.title_font)
 
    def draw_win(self) -> None:
        """Draw the victory screen."""
        self._draw_centered_text("YOU WIN!", YELLOW, self.title_font)
 
    def draw_game_over(self) -> None:
        """Draw the game over screen."""
        self._draw_centered_text("GAME OVER", RED, self.title_font)
 
    def _draw_centered_text(
        self,
        text: str,
        color: Tuple[int, int, int],
        font: Optional[pygame.font.Font] = None,
        y_offset: int = 0,
    ) -> None:
        """Draw text horizontally centred, offset vertically from centre."""
        font = font or self.font
        surface = font.render(text, True, color)
        rect = surface.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2 + y_offset)
        )
        self.screen.blit(surface, rect)
 
