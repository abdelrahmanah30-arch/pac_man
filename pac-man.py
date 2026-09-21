import sys
from pathlib import Path
import pygame

from config_loader import Configloader, ConfigValidator
from game_config import GameConfig

from maze_manager import MazeManager
from player import Player
from ghost import Ghost

from score_manager import ScoreManager
from high_score import HighScoreManager

from input_handler import InputHandler
from renderer import Renderer

from gum_manager import GumManager
from pacgum import PacgumType


class GameState:

    MENU = "MENU"
    PLAYING = "PLAYING"
    GAME_OVER = "GAME_OVER"
    WIN = "WIN"



class Game:

    def __init__(self, config):

        pygame.init()

        self.config = config
        self.state = GameState.MENU
        self.running = True


        # FPS control

        self.clock = pygame.time.Clock()

        self.ghost_move_timer = 0


        # -----------------
        # Input Handler
        # -----------------

        self.input_handler = InputHandler()



        # -----------------
        # Create Maze
        # -----------------

        self.maze = MazeManager(
            config.width,
            config.height,
            config.seed
        )

        

        #-----------------
        # PacGums
        #-----------------

        self.gum_manager = GumManager(
            self.maze
        )

        # -----------------
        # Renderer
        # -----------------

        self.renderer = Renderer(
            config.width,
            config.height
        )

        self.renderer.initialize()



        # -----------------
        # Create Player
        # -----------------

        self.player = Player(
            start_position=self.maze.find_center_start(),
            lives=config.lives
        )



        # -----------------
        # Create Ghosts
        # -----------------

        self.ghosts = [

            Ghost(
                start_position=(0, 0),
                color="blue"
            ),

            Ghost(
                start_position=(0, config.height - 1),
                color="green"
            ),
            Ghost(
                start_position=(config.width - 1, 0),
                color="orange"
            ),
            Ghost(
                start_position=(config.width - 1, config.height - 1),
                color="purple"
            )

        ]



        # -----------------
        # Score System
        # -----------------

        self.score_manager = ScoreManager(
            config
        )



        # -----------------
        # High Score
        # -----------------

        self.high_score = HighScoreManager(
            config.highscore_filename
        )

        self.high_score.load()



        print("Game initialized successfully")


    def start(self):
        

        self.state = GameState.PLAYING

        print("Game started")


        while self.running:



            if not self.input_handler.handle_input():

                self.running = False
                break



            direction = self.input_handler.get_direction()


            if direction:

                self.player.change_direction(
                    direction
                )



            self.update()

            self.render()

            self.check_game_state()



            self.clock.tick(60)



        pygame.quit()






    def update(self):

        if self.state != GameState.PLAYING:
            return


        # Player
        self.player.move(
            self.maze
        )

        self.player.update_pixel_position()

        self.player.update_mouth()

        gum = self.gum_manager.eat_gum(
            self.player.get_pixel_cell()
        )


        if gum:

            self.score_manager.add_pacgum_score(
                gum
            )
            self.player.open_mouth()
        
        if self.gum_manager.remaining() == 0:

            self.state = GameState.WIN

        if gum == PacgumType.SUPER:

            for ghost in self.ghosts:
            
                ghost.become_frightened()

        # Ghost movement timer
        self.ghost_move_timer += 1


        if self.ghost_move_timer >= 2:

            for ghost in self.ghosts:

                if not ghost.moving:

                    ghost.chase(
                        self.maze,
                        self.player.position,
                        self.ghosts
                    )

            self.ghost_move_timer = 0



        # Ghost smooth movement
        for ghost in self.ghosts:

            ghost.update_pixel_position()



        self.check_collision()
        self.player.update_mouth()



    def render(self):

        self.renderer.clear()


        if self.state == GameState.PLAYING:

            self.renderer.draw_maze(
                self.maze.maze
            )

            self.renderer.draw_gums(
                self.gum_manager.gums
            )


            self.renderer.draw_player(
                self.player
            )


            self.renderer.draw_ghosts(
                self.ghosts
            )


            self.renderer.draw_hud(
                self.score_manager.get_score(),
                self.player.lives,
                1
            )


        elif self.state == GameState.WIN:

            self.renderer.draw_win()


        elif self.state == GameState.GAME_OVER:

            self.renderer.draw_game_over()


        self.renderer.update()





    def check_collision(self):

        for ghost in self.ghosts:

            if ghost.position == self.player.position:


                if ghost.state == "FRIGHTENED":
                
                    self.score_manager.score += 200

                    ghost.reset_position()

                    ghost.become_normal()


                else:
                
                    self.player.lose_life()

                    for ghost in self.ghosts:
                        ghost.reset_position()


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



        print("\nGAME OVER")

        print(
            "Score:",
            current_score
        )


        print(
            "High Score:",
            self.high_score.get_highscore()
        )



        self.running = False







def main():


    if len(sys.argv) != 2:

        print(
            "Usage: python3 pac-man.py <config.json>"
        )

        return 1




    config_path = Path(
        sys.argv[1]
    )



    if config_path.suffix.lower() != ".json":

        print(
            "Error: configuration file must be JSON"
        )

        return 1




    if not config_path.exists():

        print(
            "Error: configuration file not found"
        )

        return 1




    try:


        loader = Configloader(
            config_path
        )


        config_data = loader.load()



        validator = ConfigValidator(
            config_data
        )


        validator.validate()



        game_config = GameConfig(
            validator
        )



        print(
            "Configuration loaded successfully"
        )



        game = Game(
            game_config
        )


        game.start()



    except Exception as error:


        print(
            "Error:",
            error
        )

        return 1




    return 0





if __name__ == "__main__":

    sys.exit(
        main()
    )