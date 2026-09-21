import pygame
from sprite_manager import SpriteManager


class Renderer:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.cell_size = 45
        self.top_bar_height = 90

        self.screen = None

        self.screen_width = 0
        self.screen_height = 0

        self.background_color = (0, 0, 0)

        self.wall_color = (0, 0, 255)
        self.floor_color = (0, 0, 0)

        self.font = None

        self.sprite_manager = SpriteManager(
            self.cell_size
        )



    def initialize(self):

        pygame.init()

        self.update_screen_size()

        self.font = pygame.font.SysFont(
            None,
            30
        )

        self.sprite_manager.load_sprites()


        pygame.display.set_caption(
            "Pac-Man 42"
        )



    def update_screen_size(self):

        self.screen_height = (
            self.height * self.cell_size
            + self.top_bar_height
        )

        self.screen_width = (
            self.width * self.cell_size
        )


        self.screen = pygame.display.set_mode(
            (
                self.screen_width,
                self.screen_height
            )
        )



    def update_size(self, width, height):

        self.width = width
        self.height = height

        self.update_screen_size()



    def clear(self):

        self.screen.fill(
            self.background_color
        )



    def update(self):

        pygame.display.flip()



    def draw_maze(self, maze):

        wall_width = 3

        height = len(maze)
        width = len(maze[0])


        for row in range(height):

            for col in range(width):

                cell = maze[row][col]


                x = col * self.cell_size

                y = (
                    row * self.cell_size
                    + self.top_bar_height
                )


                pygame.draw.rect(
                    self.screen,
                    self.floor_color,
                    (
                        x,
                        y,
                        self.cell_size,
                        self.cell_size
                    )
                )


                if cell & 1:

                    pygame.draw.line(
                        self.screen,
                        self.wall_color,
                        (x, y),
                        (x + self.cell_size, y),
                        wall_width
                    )


                if cell & 2:

                    pygame.draw.line(
                        self.screen,
                        self.wall_color,
                        (
                            x + self.cell_size,
                            y
                        ),
                        (
                            x + self.cell_size,
                            y + self.cell_size
                        ),
                        wall_width
                    )


                if cell & 4:

                    pygame.draw.line(
                        self.screen,
                        self.wall_color,
                        (
                            x,
                            y + self.cell_size
                        ),
                        (
                            x + self.cell_size,
                            y + self.cell_size
                        ),
                        wall_width
                    )


                if cell & 8:

                    pygame.draw.line(
                        self.screen,
                        self.wall_color,
                        (x, y),
                        (
                            x,
                            y + self.cell_size
                        ),
                        wall_width
                    )



    def draw_player(self, player):

        x, y = player.pixel_position

        y += self.top_bar_height


        self.screen.blit(
            self.sprite_manager.get_player(
                player.direction,
                player.mouth_open
            ),
            (x, y)
        )



    def draw_ghosts(self, ghosts):

        for ghost in ghosts:

            x, y = ghost.pixel_position

            y += self.top_bar_height


            image = self.sprite_manager.get_ghost(
                ghost.color,
                ghost.direction
            )


            if image:

                self.screen.blit(
                    image,
                    (x, y)
                )



    def draw_gums(self, gums):

        for position, gum_type in gums.items():

            row, col = position


            x = (
                col * self.cell_size
                + self.cell_size // 2
            )


            y = (
                row * self.cell_size
                + self.cell_size // 2
                + self.top_bar_height
            )


            radius = 4


            if str(gum_type) == "PacgumType.SUPER":

                radius = 9


            pygame.draw.circle(
                self.screen,
                (255,255,255),
                (x,y),
                radius
            )



    def draw_hud(self, score, lives, level):

        score_text = self.font.render(
            f"Score: {score}",
            True,
            (255,255,255)
        )


        level_text = self.font.render(
            f"Level: {level}",
            True,
            (255,255,255)
        )


        lives_text = self.font.render(
            f"Lives: {lives}",
            True,
            (255,255,255)
        )


        self.screen.blit(
            score_text,
            (20,20)
        )


        self.screen.blit(
            level_text,
            (250,20)
        )


        self.screen.blit(
            lives_text,
            (450,20)
        )



    def draw_win(self):

        text = self.font.render(
            "YOU WIN!",
            True,
            (255,255,0)
        )


        rect = text.get_rect(
            center=(
                self.screen_width // 2,
                self.screen_height // 2
            )
        )


        self.screen.blit(
            text,
            rect
        )



    def draw_game_over(self):

        text = self.font.render(
            "GAME OVER",
            True,
            (255,0,0)
        )


        rect = text.get_rect(
            center=(
                self.screen_width // 2,
                self.screen_height // 2
            )
        )


        self.screen.blit(
            text,
            rect
        )
    
    def update_size(self, width, height):

        self.width = width
        self.height = height

        self.screen_height = (
            height * self.cell_size
            + self.top_bar_height
        )

        self.screen_width = (
            width * self.cell_size
        )

        self.screen = pygame.display.set_mode(
            (
                self.screen_width,
                self.screen_height
            )
        )