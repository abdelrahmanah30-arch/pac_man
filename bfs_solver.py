from collections import deque


class BFSSolver:

    def __init__(self):
        pass


    def find_path(self, maze, start, goal):
        """
        Find shortest path from start to goal using BFS

        start = (row, col)
        goal  = (row, col)

        return:
            list of positions
        """

        queue = deque()

        visited = set()

        parent = {}

        queue.append(start)
        visited.add(start)

        while queue:

            current = queue.popleft()

            if current == goal:
                return self.reconstruct_path(parent, start, goal)


            for neighbor in self.get_neighbors(maze, current):

                if neighbor not in visited:
                    visited.add(neighbor)

                    parent[neighbor] = current

                    queue.append(neighbor)


        return []


    def get_neighbors(self, maze, position):

        row, col = position

        neighbors = [

            (row - 1, col),

            (row + 1, col),

            (row, col - 1),

            (row, col + 1)
        ]


        valid_neighbors = []

        for cell in neighbors:

            if maze.is_valid_position(cell):
                valid_neighbors.append(cell)


        return valid_neighbors



    def reconstruct_path(self, parent, start, goal):

        path = []

        current = goal


        while current != start:

            path.append(current)

            current = parent[current]


        path.append(start)


        path.reverse()


        return path