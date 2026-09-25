from collections import deque
from direction import Direction


class ReverseBFSSolver:

    def calculate_distances(self, maze, start):

        queue = deque()

        distances = {}

        queue.append(start)
        distances[start] = 0


        while queue:

            current = queue.popleft()

            for neighbor in self.get_neighbors(
                maze,
                current
            ):

                if neighbor not in distances:

                    distances[neighbor] = (
                        distances[current] + 1
                    )

                    queue.append(neighbor)


        return distances



    def get_neighbors(self, maze, position):

        row, col = position


        neighbors = [

            (
                (row - 1, col),
                Direction.UP
            ),

            (
                (row + 1, col),
                Direction.DOWN
            ),

            (
                (row, col - 1),
                Direction.LEFT
            ),

            (
                (row, col + 1),
                Direction.RIGHT
            )

        ]


        valid_neighbors = []


        for cell, direction in neighbors:

            if maze.is_valid_position(
                position,
                direction
            ):

                valid_neighbors.append(cell)


        return valid_neighbors