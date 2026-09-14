import sys
from pathlib import Path

from config_loader import Configloader, ConfigValidator
from game_config import GameConfig

from maze_manager import MazeManager
from player import Player
from ghost import Ghost

from score_manager import ScoreManager
from high_score import HighScoreManager


class GameState:
    MENU = "MENU"
    PLAYING = "PLAYING"
    GAME_OVER = "GAME_OVER"
    WIN = "WIN"


class Game:

    def __init__(self, config):

        self.config = config

        # Game state
        self.state = GameState.MENU
        self.running = True


        # Maze
        self.maze = MazeManager(
            config.width,
            config.height,
            config.seed
        )


        # Player start position
        # مؤقت إلى أن يصبح عندنا Maze Generator
        self.player = Player(
            start_position=(1, 1),
            lives=config.lives
        )


        # Ghosts
        self.ghosts = [

            Ghost(
                start_position=(5, 5),
                color="red"
            ),

            Ghost(
                start_position=(5, 6),
                color="blue"
            )
        ]


        # Score
        self.score_manager = ScoreManager(config)


        # High Score
        self.high_score = HighScoreManager(
            config.highscore_filename
        )

        self.high_score.load()



    def start(self):

        self.state = GameState.PLAYING

        while self.running:

            self.update()

            self.check_game_state()



    def update(self):

        if self.state != GameState.PLAYING:
            return


        # Player movement
        self.player.move(self.maze)


        # Ghost movement
        for ghost in self.ghosts:

            ghost.chase(
                self.maze,
                self.player.position
            )


        # Collision
        self.check_collision()



    def check_collision(self):

        for ghost in self.ghosts:

            if ghost.position == self.player.position:

                self.player.lose_life()

                break



    def check_game_state(self):

        if not self.player.is_alive():

            self.game_over()



    def game_over(self):

        self.state = GameState.GAME_OVER


        current_score = self.score_manager.get_score()


        self.high_score.update(
            current_score
        )


        print("GAME OVER")
        print("Score:", current_score)
        print(
            "High Score:",
            self.high_score.get_highscore()
        )


        self.running = False



def main():

    if len(sys.argv) != 2:

        print(
            "Usage: python3 pac-man.py config.json"
        )

        return 1


    config_path = Path(sys.argv[1])


    if config_path.suffix.lower() != ".json":

        print(
            "Error: configuration file must be JSON"
        )

        return 1



    if not config_path.exists():

        print(
            "Error: file not found"
        )

        return 1



    loader = Configloader(config_path)

    config_data = loader.load()


    validator = ConfigValidator(config_data)

    validator.validate()


    game_config = GameConfig(
        validator
    )


    game = Game(
        game_config
    )


    game.start()


    return 0



if __name__ == "__main__":
    sys.exit(main())