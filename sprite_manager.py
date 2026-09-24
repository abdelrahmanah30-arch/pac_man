import pygame


class SpriteManager:

    def __init__(self, cell_size):

        self.cell_size = cell_size

        self.ghosts = {}
        self.frightened_ghosts = {}
        self.ghost_eyes = {}

        self.player_open = None
        self.player_close = None



    def load_sprites(self):

        # Player

        self.player_close = pygame.image.load(
            "assets/player/close.png"
        )

        self.player_open = pygame.image.load(
            "assets/player/pacman.png"
        )


        self.player_open = pygame.transform.scale(
            self.player_open,
            (
                self.cell_size,
                self.cell_size
            )
        )


        self.player_close = pygame.transform.scale(
            self.player_close,
            (
                self.cell_size,
                self.cell_size
            )
        )



        # Ghosts

        colors = [
            "blue",
            "green",
            "orange",
            "purple"
        ]


        directions = [
            "up",
            "down",
            "left",
            "right"
        ]

        for direction in directions:
            image = pygame.image.load(
                f"assets/ghosts/eye_{direction}.png"
            )

            image = pygame.transform.scale(
                image,
                (
                    self.cell_size,
                    self.cell_size
                )
            )

            self.ghost_eyes[direction.upper()] = image

        for color in colors:

            self.ghosts[color] = {}
            self.frightened_ghosts[color] = {}


            for direction in directions:


                image = pygame.image.load(
                    f"assets/ghosts/{color}_{direction}.png"
                )


                image = pygame.transform.scale(
                    image,
                    (
                        self.cell_size,
                        self.cell_size
                    )
                )


                self.ghosts[color][direction.upper()] = image



                # Create frightened version

                frightened = image.copy()


                frightened.fill(
                    (100, 150, 255),
                    special_flags=pygame.BLEND_RGB_MULT
                )


                self.frightened_ghosts[color][direction.upper()] = frightened




    def get_player(self, direction=None, mouth_open=False):

        if mouth_open:

            image = self.player_open

        else:

            image = self.player_close



        if direction is None:

            return image



        if direction.name == "LEFT":

            image = pygame.transform.rotate(
                image,
                180
            )


        elif direction.name == "UP":

            image = pygame.transform.rotate(
                image,
                90
            )


        elif direction.name == "DOWN":

            image = pygame.transform.rotate(
                image,
                -90
            )


        return image




    def get_ghost(
        self,
        color,
        direction,
        state="NORMAL"
    ):

        if state == "EATEN":
            return self.ghost_eyes[direction]

        if state == "FRIGHTENED":

            return self.frightened_ghosts[color][direction]


        return self.ghosts[color][direction]