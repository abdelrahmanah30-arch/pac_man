import pygame
from sprite_manager import SpriteManager

class Renderer:
    def __init__(self, width, height):
    
        self.width = width
        self.height = height
    
        self.screen = None
    
        self.cell_size = 45
    
        self.sprite_manager = SpriteManager(
           self.cell_size
        )

        self.screen_width = None
        self.screen_height = None
    
        self.background_color = None
    
        self.wall_color = (0, 0, 255)
        self.floor_color = (0, 0, 0)

        self.player_color = (255, 255, 0)

        self.ghost_colors = {
           "red": (255, 0, 0),
            "blue": (0, 0, 255)
        }
    
        self.clock = None
        self.font = None

    def initialize(self):

        pygame.init()

        self.screen_height = self.height * self.cell_size
        self.screen_width = self.width * self.cell_size


        self.screen = pygame.display.set_mode(
            (
                self.screen_width,
                self.screen_height
            )
        )


        self.sprite_manager.load_sprites()


        pygame.display.set_caption(
            "Pac-Man 42"
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
                y = row * self.cell_size
    
    
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

        print("SCREEN:", self.screen)
        print("PLAYER IMAGE:", self.sprite_manager.get_player())

        row, col = player.position

        x = col * self.cell_size
        y = row * self.cell_size

        self.screen.blit(
            self.sprite_manager.get_player(),
            (x,y)
        )
        print(self.sprite_manager.get_player().get_size())

    def draw_ghosts(self, ghosts):
    
        for ghost in ghosts:
        
            row, col = ghost.position
    
    
            x = col * self.cell_size
            y = row * self.cell_size
    
    
            image = self.sprite_manager.get_ghost(
                ghost.color
            )
    
    
            if image is None:
                continue
            
            
            self.screen.blit(
                image,
                (x, y)
            )