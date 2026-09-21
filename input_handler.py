from direction import Direction
import pygame

class InputHandler:
    def __init__(self):
        self.direction = None
        self.next_level_pressed = False

    def handle_input(self):

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:


                if event.key == pygame.K_F1:

                    self.next_level_pressed = True


                elif event.key == pygame.K_UP:
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

    def get_next_level(self):

        if self.next_level_pressed:

            self.next_level_pressed = False

            return True

        return False