import heapq

# start: (x, y) tuple
# goal: (x, y) tuple
def manhattan_distance(start, goal):
    return abs(start[0] - goal[0]) + abs(start[1] - goal[1])


class Node:
    def __init__(self, position, cost, heuristic, parent=None):
        self.position = position
        self.world_position = (0, 0)
        self.parent = parent
        self.g = cost
        self.h = heuristic
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.g + self.h < other.g + other.h


class AStar:
    def __init__(self, grid, columns):
        self.grid = grid
        self.grid_columns = columns
        self.open_list = []
        self.closed_list = []
        self.path = []
        self.path_found = False
        self.path_cost = 0
        self.path_length = 0

    def find_path(self, start, goal):
        self.open_list = []
        self.closed_list = []
        start_grid_info = self.get_grid_info(start)
        start_node = Node(start, 0, manhattan_distance(start, goal))
        start_node.world_position = start_grid_info[0]
        heapq.heappush(self.open_list, start_node)
        while self.open_list:
            current_node = heapq.heappop(self.open_list)
            self.closed_list.append(current_node)
            if current_node.position == goal:
                self.path_found = True
                self.path_cost = current_node.g
                self.path = self.reconstruct_path(current_node)
                self.path_length = len(self.path)
                break
            for neighbor in self.get_neighbors(current_node, goal):
                if neighbor in self.closed_list:
                    continue
                if neighbor not in self.open_list:
                    heapq.heappush(self.open_list, neighbor)
                else:
                    if neighbor.g > current_node.g + 1:
                        neighbor.g = current_node.g + 1
                        neighbor.parent = current_node
        return self.path_found

    def get_grid_info(self, position):
        x, y = position
        index = x + y * self.grid_columns
        if 0 <= index < len(self.grid):
            return self.grid[index]
        return None

    def get_neighbors(self, node, goal):
        neighbors = []
        x, y = node.position
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            neighbor_pos = (x + dx, y + dy)
            # if the index is within the bounds of the grid
            grid_info = self.get_grid_info(neighbor_pos)
            if grid_info is not None:
                world_pos, cost = grid_info
                neighbor_node = Node(
                    neighbor_pos,
                    node.g + cost,
                    manhattan_distance(neighbor_pos, goal),
                    parent=node
                )
                neighbor_node.world_position = world_pos
                neighbors.append(neighbor_node)
        return neighbors

    def reconstruct_path(self, node):
        path = []
        while node:
            path.append(node.world_position)
            node = node.parent
        return path[::-1]
