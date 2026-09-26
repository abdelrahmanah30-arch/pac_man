import sys
from enum import Enum
from pathlib import Path
from typing import List
 
import pygame
 
from config_loader import ConfigError, ConfigLoader, ConfigValidator
from game_config import GameConfig
from ghost import Ghost, GhostState
from ghost_manager import GhostManager
from gum_manager import GumManager
from high_score import HighScoreManager
from input_handler import InputHandler
from level_manager import LevelManager
from maze_manager import MazeGenerationError, MazeManager
from pacgum import PacgumType
from player import Player
from renderer import Renderer
from score_manager import ScoreManager
 
FPS = 60
FRIGHTENED_DURATION_TICKS = 900
FRIGHTENED_RETARGET_INTERVAL_TICKS = 120
GHOST_COLORS = ["blue", "green", "orange", "purple"]
 
# TODO(teammate): this default is a stand-in until the Game Over /
# Victory screen collects a real name from the player.
PLACEHOLDER_PLAYER_NAME = "PLAYER"
 
 
class GameState(Enum):
    """The overall screen/phase the game is currently in."""
 
    MENU = "MENU"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    GAME_OVER = "GAME_OVER"
    WIN = "WIN"
 
 
class Game:
    """Owns the game loop and every subsystem it coordinates."""
 
    def __init__(self, config: GameConfig) -> None:
        """Set up pygame and every subsystem for a fresh game.
 
        Args:
            config: The validated game configuration.
        """
        pygame.init()
 
        self.config = config
        self.state = GameState.MENU
        self.running = True
 
        self.clock = pygame.time.Clock()
        self.ghost_move_timer = 0
        self.frightened_timer = 0
        self.frightened_update_timer = 0
        self.level_timer = 0
 
        self.ghost_manager = GhostManager()
        self.level_manager = LevelManager(config)
        self.input_handler = InputHandler()
 
        self.setup_level()
 
        width, height = self.level_manager.get_maze_size()
        self.renderer = Renderer(width, height)
        self.renderer.initialize()
 
        self.score_manager = ScoreManager(config)
 
        self.high_score = HighScoreManager(config.highscore_filename)
        self.high_score.load()
 
        print("Game initialized successfully")
 
    # -------------------------
    # Level Setup
    # -------------------------
 
    def setup_level(self) -> None:
        """Build a fresh maze, player, ghosts and gums for this level."""
        self.maze = self.create_maze()
        player_start = self.maze.find_center_start()
 
        self.player = Player(
            start_position=player_start,
            lives=self.config.lives,
        )
 
        self.ghosts = self.create_ghosts()
 
        self.gum_manager = GumManager(
            self.maze,
            self.player.start_position,
            self.ghosts,
        )
 
        self.ghost_move_timer = 0
        self.frightened_timer = 0
        self.frightened_update_timer = 0
        self.level_timer = self.config.level_max_time * FPS
 
    def create_maze(self) -> MazeManager:
        """Generate this level's maze from the level manager's settings."""
        width, height = self.level_manager.get_maze_size()
        seed = self.level_manager.get_seed()
 
        return MazeManager(width, height, seed)
 
    def create_ghosts(self) -> List[Ghost]:
        """Spawn the 4 ghosts at the maze's corner positions."""
        positions = self.maze.find_ghost_positions(len(GHOST_COLORS))
 
        return [
            Ghost(start_position=position, color=color)
            for position, color in zip(positions, GHOST_COLORS)
        ]
 
    # -------------------------
    # Game Loop
    # -------------------------
 
    def start(self) -> None:
        """Run the main loop until the window is closed."""
        print("Game started")
 
        while self.running:
            if not self.input_handler.handle_input():
                self.running = False
                break
 
            self._handle_state_transitions()
 
            if self.state == GameState.PLAYING:
                self._handle_playing_input()
                self.update()
 
            self.render()
            self.check_game_state()
 
            self.clock.tick(FPS)
 
        pygame.quit()
 
    def _handle_state_transitions(self) -> None:
        """Handle input that switches between screens (menu/pause).
 
        Note:
            MENU here only supports "press confirm to play", as a
            minimal placeholder. The full Main Menu (Start Game/View
            Highscores/Instructions/Exit) is a separate feature.
        """
        if self.state == GameState.MENU and self.input_handler.get_confirm():
            self.start_new_game()
        elif self.state == GameState.PLAYING and self.input_handler.get_pause():
            self.state = GameState.PAUSED
        elif self.state == GameState.PAUSED and self.input_handler.get_pause():
            self.state = GameState.PLAYING
        elif (
            self.state in (GameState.GAME_OVER, GameState.WIN)
            and self.input_handler.get_confirm()
        ):
            self.state = GameState.MENU
 
    def _handle_playing_input(self) -> None:
        """Apply movement and the debug next-level shortcut."""
        direction = self.input_handler.get_direction()
 
        if direction:
            self.player.change_direction(direction)
 
        if self.input_handler.get_next_level():
            self.next_level()
 
    def start_new_game(self) -> None:
        """Reset progress and (re)build the first level."""
        self.level_manager.level = 1
        self.score_manager.reset()
        self.setup_level()
        self.state = GameState.PLAYING
 
    # -------------------------
    # Next Level
    # -------------------------
 
    def next_level(self) -> None:
        """Advance to the next level, or win the game on the last one."""
        if not self.level_manager.next_level():
            self.win()
            return
 
        self.setup_level()
 
        width, height = self.level_manager.get_maze_size()
        self.renderer.update_size(width, height)
 
        print("Current Level:", self.level_manager.get_level())
 
    # -------------------------
    # Update
    # -------------------------
 
    def update(self) -> None:
        """Advance the simulation by one tick."""
        self.player.move(self.maze)
        self.player.update_pixel_position()
 
        self._handle_gum_pickup()
        self._update_level_timer()
        self._update_frightened_timer()
        self._update_ghosts()
 
        self.player.update_mouth()
        self.check_collision()
 
    def _handle_gum_pickup(self) -> None:
        """Eat any gum under the player and react to super-pacgums."""
        gum = self.gum_manager.eat_gum(self.player.get_pixel_cell())
 
        if gum is None:
            return
 
        self.score_manager.add_pacgum_score(gum)
        self.player.open_mouth()
 
        if gum == PacgumType.SUPER:
            for ghost in self.ghosts:
                ghost.become_frightened()
 
            self.update_frightened_targets()
            self.frightened_update_timer = FRIGHTENED_RETARGET_INTERVAL_TICKS
            self.frightened_timer = FRIGHTENED_DURATION_TICKS
 
        if self.gum_manager.remaining() == 0:
            self.next_level()
 
    def _update_level_timer(self) -> None:
        """Count down the level's time limit; react when it hits zero."""
        self.level_timer -= 1
 
        if self.level_timer <= 0:
            self.handle_level_timeout()
 
    def handle_level_timeout(self) -> None:
        """Handle the level's time limit being reached.
 
        Chosen behaviour: the player loses a life and the level
        resets, matching what happens when a ghost catches them (the
        subject leaves this choice open).
        """
        self.player.lose_life()
 
        for ghost in self.ghosts:
            ghost.reset_position()
 
        self.level_timer = self.config.level_max_time * FPS
 
    def _update_frightened_timer(self) -> None:
        """Count down FRIGHTENED mode and end it when it expires."""
        if self.frightened_timer <= 0:
            return
 
        self.frightened_timer -= 1
        self.frightened_update_timer -= 1
 
        if self.frightened_update_timer <= 0:
            self.update_frightened_targets()
            self.frightened_update_timer = FRIGHTENED_RETARGET_INTERVAL_TICKS
 
        if self.frightened_timer <= 0:
            for ghost in self.ghosts:
                if ghost.state == GhostState.FRIGHTENED:
                    ghost.become_normal()
 
    def _update_ghosts(self) -> None:
        """Move every ghost every other tick, then advance their animation."""
        self.ghost_move_timer += 1
 
        if self.ghost_move_timer >= 2:
            for ghost in self.ghosts:
                if not ghost.moving:
                    ghost.chase(self.maze, self.player.position, self.ghosts)
 
            self.ghost_move_timer = 0
 
        for ghost in self.ghosts:
            ghost.update_pixel_position()
 
        for ghost in self.ghosts:
            ghost.update()
 
    def update_frightened_targets(self) -> None:
        """Re-assign escape targets to every currently FRIGHTENED ghost."""
        frightened_ghosts = [
            ghost for ghost in self.ghosts if ghost.state == GhostState.FRIGHTENED
        ]
 
        if not frightened_ghosts:
            return
 
        self.ghost_manager.update_frightened_targets(
            frightened_ghosts,
            self.maze,
            self.player.position,
        )
 
    # -------------------------
    # Render
    # -------------------------
 
    def render(self) -> None:
        """Draw whichever screen matches the current game state."""
        self.renderer.clear()
 
        if self.state == GameState.MENU:
            self.renderer.draw_menu(self.high_score.get_top_scores())
        elif self.state in (GameState.PLAYING, GameState.PAUSED):
            self.renderer.draw_maze(self.maze.maze)
            self.renderer.draw_gums(self.gum_manager.gums)
            self.renderer.draw_player(self.player)
            self.renderer.draw_ghosts(self.ghosts)
            self.renderer.draw_hud(
                self.score_manager.get_score(),
                self.player.lives,
                self.level_manager.get_level(),
                self.level_timer // FPS,
            )
            if self.state == GameState.PAUSED:
                self.renderer.draw_pause()
        elif self.state == GameState.WIN:
            self.renderer.draw_win()
        elif self.state == GameState.GAME_OVER:
            self.renderer.draw_game_over()
 
        self.renderer.update()
 
    # -------------------------
    # Collision
    # -------------------------
 
    def check_collision(self) -> None:
        """Resolve the player touching a ghost this tick, if any."""
        for ghost in self.ghosts:
            if ghost.state in (GhostState.EATEN, GhostState.WAITING):
                continue
 
            if ghost.get_pixel_cell() != self.player.get_pixel_cell():
                continue
 
            if ghost.state == GhostState.FRIGHTENED:
                self.score_manager.add_ghost_score()
                ghost.become_eaten()
            else:
                self.player.lose_life()
                for other_ghost in self.ghosts:
                    other_ghost.reset_position()
 
            break
 
    def check_game_state(self) -> None:
        """Check whether the player has just run out of lives."""
        if self.state == GameState.PLAYING and not self.player.is_alive():
            self.game_over()
 
    def game_over(self) -> None:
        """Handle the player losing their last life."""
        self.state = GameState.GAME_OVER
        self._record_score()
 
        print("GAME OVER")
        print("Score:", self.score_manager.get_score())
        print("High Score:", self.high_score.get_highscore())
 
    def win(self) -> None:
        """Handle the player completing every level."""
        self.state = GameState.WIN
        self._record_score()
 
        print("Congratulations! You finished all levels.")
 
    def _record_score(self) -> None:
        """Save this run's score to the highscore list."""
        score = self.score_manager.get_score()
        self.high_score.add_score(PLACEHOLDER_PLAYER_NAME, score)
        self.high_score.save()
 
 
def main() -> int:
    """Parse arguments, load the config, and run the game.
 
    Returns:
        0 on a clean exit, 1 if something went wrong.
    """
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py <config.json>")
        return 1
 
    config_path = Path(sys.argv[1])
 
    if config_path.suffix.lower() != ".json":
        print("Error: configuration file must be JSON")
        return 1
 
    if not config_path.exists():
        print("Error: configuration file not found")
        return 1
 
    try:
        config_data = ConfigLoader(config_path).load()
 
        validator = ConfigValidator(config_data)
        validator.validate()
 
        game_config = GameConfig(validator)
        print("Configuration loaded successfully")
 
        game = Game(game_config)
        game.start()
    except (ConfigError, MazeGenerationError) as error:
        print("Error:", error)
        return 1
    except Exception as error:
        print("Error:", error)
        return 1
 
    return 0
 
 
if __name__ == "__main__":
    sys.exit(main())
 
