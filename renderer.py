import pygame
from sprite_manager import SpriteManager


class Renderer:
    def __init__(self, width, height):
    
        self.width = width
        self.height = height
    
        self.screen = None

    
        self.cell_size = 45
        self.top_bar_height = 90
    
        self.sprite_manager = SpriteManager(
           self.cell_size
        )

        self.screen_width = None
        self.screen_height = None
    
        self.background_color = None
    
        self.wall_color = (0, 0, 255)
        self.floor_color = (0, 0, 0)

        self.player_color = (255, 255, 0)


        
        self.clock = None
        self.font = None

    def initialize(self):

        pygame.init()

        self.screen_height = (
            self.height * self.cell_size
            + self.top_bar_height
        )
        self.screen_width = self.width * self.cell_size


        self.screen = pygame.display.set_mode(
            (
                self.screen_width,
                self.screen_height
            )
        )

        self.font = pygame.font.SysFont(
            None,
            30
        )
        self.sprite_manager.load_sprites()


        pygame.display.set_caption(
            "Pac-Man 42"
        )

        self.font = pygame.font.SysFont(
            None,
            30
        )


        self.background_color = (0, 0, 0)

    def clear(self):
        self.screen.fill(self.background_color)

    def update(self):
        pygame.display.flip()

    def draw_maze(self, maze):

        wall_width = 3
    
        for row in range(self.height):
        
            for col in range(self.width):
            
                cell = maze[row][col]
    
                x = col * self.cell_size
                y = (
                    row * self.cell_size
                    + self.top_bar_height
                )
    
    
                # draw floor
    
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
    
    
                # draw walls from bitmask
    
                if cell & 1:   # top
                
                    pygame.draw.line(
                        self.screen,
                        self.wall_color,
                        (x, y),
                        (x + self.cell_size, y),
                        wall_width
                    )
    
    
                if cell & 2:   # right
                
                    pygame.draw.line(
                        self.screen,
                        self.wall_color,
                        (x + self.cell_size, y),
                        (x + self.cell_size, y + self.cell_size),
                        wall_width
                    )
    
    
                if cell & 4:   # bottom
                
                    pygame.draw.line(
                        self.screen,
                        self.wall_color,
                        (x, y + self.cell_size),
                        (x + self.cell_size, y + self.cell_size),
                        wall_width
                    )
    
    
                if cell & 8:   # left
                
                    pygame.draw.line(
                        self.screen,
                        self.wall_color,
                        (x, y),
                        (x, y + self.cell_size),
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
            (x,y)
        )

    def draw_ghosts(self, ghosts):
    
        for ghost in ghosts:


            x, y = ghost.pixel_position
            y += self.top_bar_height
    
    
            image = self.sprite_manager.get_ghost(
                ghost.color,
                ghost.direction
            )
    
    
            if image is None:
                continue
            
            
            self.screen.blit(
                image,
                (x, y)
            )

    def draw_gums(self, gums):

        for row, col in gums:

            x = col * self.cell_size + self.cell_size // 2
            y = (
                row * self.cell_size
                + self.cell_size // 2
                + self.top_bar_height
            )


            pygame.draw.circle(
                self.screen,
                (255,255,255),
                (x,y),
                4
            )

    def draw_score(self, score):

        text = self.font.render(
            f"Score: {score}",
            True,
            (255,255,255)
        )

        self.screen.blit(
            text,
            (10,10)
         )

    def draw_lives(self, lives):

        text = self.font.render(
            f"Lives: {lives}",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            text,
            (10, 40)
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
    
    
        self.screen.blit(score_text, (20,20))
        self.screen.blit(level_text, (400,20))
        self.screen.blit(lives_text, (700,20))