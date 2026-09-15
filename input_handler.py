from direction import Direction
import pygame

class InputHandler:
    def __init__(self):
        self.direction = None

    def handle_input(self):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    self.direction = Direction.UP

                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT

                elif event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT

            elif event.type == pygame.QUIT:
                return False

        return True

    def get_direction(self):
        return self.direction