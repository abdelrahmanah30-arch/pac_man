from mazegenerator.mazegenerator import MazeGenerator
from direction import Direction


class MazeManager:

    def __init__(self, width, height, seed):

        self.width = width
        self.height = height
        self.seed = seed

        self.generator = None
        self.maze = None

        self.generate()


    def generate(self):

        self.generator = MazeGenerator(
            size=(self.width, self.height),
            seed=self.seed
        )

        self.generator.generate(
            self.seed
        )

        self.maze = self.generator.maze



    def find_center_start(self):

        center_row = self.height // 2
        center_col = self.width // 2


        positions = []


        for radius in range(
            max(self.width, self.height)
        ):

            for row in range(
                center_row - radius,
                center_row + radius + 1
            ):

                for col in range(
                    center_col - radius,
                    center_col + radius + 1
                ):

                    positions.append(
                        (row, col)
                    )



        for position in positions:

            if self.can_spawn(position):

                return position



        return (1, 1)



    def can_spawn(self, position):

        if not self.is_valid_position(position):

            return False



        open_paths = self.get_open_neighbors(
            position
        )


        return open_paths > 0




    def is_valid_position(self, position, direction=None):

        row, col = position


        if row < 0 or row >= self.height:

            return False


        if col < 0 or col >= self.width:

            return False



        current = self.maze[row][col]



        if direction == Direction.UP:

            if current & 1:

                return False



        elif direction == Direction.RIGHT:

            if current & 2:

                return False



        elif direction == Direction.DOWN:

            if current & 4:

                return False



        elif direction == Direction.LEFT:

            if current & 8:

                return False



        return True




    def get_open_neighbors(self, position):

        directions = [

            Direction.UP,
            Direction.RIGHT,
            Direction.DOWN,
            Direction.LEFT

        ]


        count = 0


        for direction in directions:

            if self.is_valid_position(
                position,
                direction
            ):

                count += 1



        return count

    def find_ghost_positions(self, count=4):
    
        positions = []
    
    
        corners = [
        
            (1, 1),
    
            (1, self.width - 2),
    
            (self.height - 2, 1),
    
            (self.height - 2, self.width - 2)
    
        ]
    
    
        for position in corners:
        
            if self.can_spawn(position):
            
                positions.append(position)
    
    
    
        # إذا لم نجد 4 أماكن، نبحث في باقي الخريطة
    
        if len(positions) < count:
        
        
            for row in range(self.height):
            
                for col in range(self.width):
                
                    position = (row, col)
    
    
                    if (
                        self.can_spawn(position)
                        and position not in positions
                    ):
    
                        positions.append(position)
    
    
                    if len(positions) == count:
                    
                        return positions
    
    
    
        return positions