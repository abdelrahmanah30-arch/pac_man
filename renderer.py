import pygame

class Renderer:
    def __init__(self, width, height):
    
        self.width = width
        self.height = height
    
        self.screen = None
    
        self.cell_size = 32
    
        self.screen_width = None
        self.screen_height = None
    
        self.background_color = None
    
        self.wall_color = (0, 0, 255)
        self.floor_color = (0, 0, 0)
    
        self.clock = None
        self.font = None

    def initialize(self):
        
        pygame.init()
        
        self.screen_height = self.height * self.cell_size
        self.screen_width = self.width * self.cell_size

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )

        pygame.display.set_caption("Pac-Man 42")

        self.background_color = (0, 0, 0)

    def clear(self):
        self.screen.fill(self.background_color)

    def update(self):
        pygame.display.flip()

    def draw_maze(self, maze):

        for row in range(self.height):

            for col in range(self.width):

                cell = maze[row][col]

                x = col * self.cell_size
                y = row * self.cell_size

                if cell == "#":

                    pygame.draw.rect(
                        self.screen,
                        self.wall_color,
                        (
                            x,
                            y,
                            self.cell_size,
                            self.cell_size
                        )
                    )

                else:

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