import pygame


class SpriteManager:

    def __init__(self, cell_size):

        self.cell_size = cell_size

        self.player = None

        self.ghosts = {}



    def load_sprites(self):

        # Player

        self.player = pygame.image.load(
            "assets/player/pacman.png"
        )

        self.player = pygame.transform.scale(
            self.player,
            (
                self.cell_size,
                self.cell_size
            )
        )



        # Ghosts

        self.ghosts["red"] = pygame.image.load(
            "assets/ghosts/red.png"
        )

        self.ghosts["blue"] = pygame.image.load(
            "assets/ghosts/blue.png"
        )


        for color in self.ghosts:

            self.ghosts[color] = pygame.transform.scale(
                self.ghosts[color],
                (
                    self.cell_size,
                    self.cell_size
                )
            )



    def get_player(self):

        return self.player



    def get_ghost(self, color):

        return self.ghosts.get(color)