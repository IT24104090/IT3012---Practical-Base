from collections import deque
import heapq
import math


class SearchAgent:
    """
    Search-based agent supporting BFS, DFS, UCS and A*.
    """

    def __init__(self):
        self.plan = []
        self.active_algo = "AStar"     # Default algorithm

    # ==================================================
    # Heuristic Functions
    # ==================================================

    def manhattan_distance(self, pos, goal):
        """
        Manhattan Distance:
        h(n) = |x1 - x2| + |y1 - y2|
        """
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def euclidean_distance(self, pos, goal):
        """
        Euclidean Distance:
        h(n) = sqrt((x1 - x2)^2 + (y1 - y2)^2)
        """
        return math.sqrt(
            (pos[0] - goal[0]) ** 2 +
            (pos[1] - goal[1]) ** 2
        )

    # ==================================================
    # Get Neighbors
    # ==================================================

    def get_neighbors(self, state, walls, width, height):

        x, y = state

        moves = [
            ("Up", (x, y + 1)),
            ("Down", (x, y - 1)),
            ("Left", (x - 1, y)),
            ("Right", (x + 1, y))
        ]

        valid = []

        for action, (nx, ny) in moves:

            if (
                0 <= nx < width and
                0 <= ny < height and
                (nx, ny) not in walls
            ):
                valid.append((action, (nx, ny)))

        return valid

    # ==================================================
    # BFS
    # ==================================================

    def bfs_search(self, start, goals, walls, width, height):

        frontier = deque()
        frontier.append((start, []))

        reached = {start}

        while frontier:

            state, path = frontier.popleft()

            if state in goals:
                return path

            for action, next_state in self.get_neighbors(
                    state, walls, width, height):

                if next_state not in reached:
                    reached.add(next_state)

                    frontier.append(
                        (next_state, path + [action])
                    )

        return []

    # ==================================================
    # DFS
    # ==================================================

    def dfs_search(self, start, goals, walls, width, height):

        frontier = [(start, [])]

        reached = {start}

        while frontier:

            state, path = frontier.pop()

            if state in goals:
                return path

            for action, next_state in self.get_neighbors(
                    state, walls, width, height):

                if next_state not in reached:
                    reached.add(next_state)

                    frontier.append(
                        (next_state, path + [action])
                    )

        return []

    # ==================================================
    # UCS
    # ==================================================

    def ucs_search(self, start, goals, walls, width, height):

        frontier = []

        heapq.heappush(
            frontier,
            (0, start, [])
        )

        reached = set()

        while frontier:

            cost, state, path = heapq.heappop(frontier)

            if state in reached:
                continue

            reached.add(state)

            if state in goals:
                return path

            for action, next_state in self.get_neighbors(
                    state, walls, width, height):

                if next_state not in reached:

                    new_cost = cost + 1

                    heapq.heappush(
                        frontier,
                        (
                            new_cost,
                            next_state,
                            path + [action]
                        )
                    )

        return []

    # ==================================================
    # A* Search
    # ==================================================

    def astar_search(
            self,
            start_pos,
            goal_pos,
            walls,
            grid_size,
            heuristic_type='manhattan'):

        width, height = grid_size

        priority_queue = []
        reached_states = set()

        # Initial heuristic value
        if heuristic_type == "euclidean":
            h_cost = self.euclidean_distance(
                start_pos,
                goal_pos
            )
        else:
            h_cost = self.manhattan_distance(
                start_pos,
                goal_pos
            )

        g_cost = 0
        f_cost = g_cost + h_cost

        heapq.heappush(
            priority_queue,
            (
                f_cost,
                g_cost,
                start_pos,
                []
            )
        )

        while priority_queue:

            f_cost, g_cost, current_pos, path_taken = \
                heapq.heappop(priority_queue)

            if current_pos == goal_pos:
                return path_taken

            if current_pos in reached_states:
                continue

            reached_states.add(current_pos)

            for action, neighbor in self.get_neighbors(
                    current_pos,
                    walls,
                    width,
                    height):

                if neighbor in reached_states:
                    continue

                new_g = g_cost + 1

                if heuristic_type == "euclidean":
                    new_h = self.euclidean_distance(
                        neighbor,
                        goal_pos
                    )
                else:
                    new_h = self.manhattan_distance(
                        neighbor,
                        goal_pos
                    )

                new_f = new_g + new_h

                heapq.heappush(
                    priority_queue,
                    (
                        new_f,
                        new_g,
                        neighbor,
                        path_taken + [action]
                    )
                )

        return []

    # ==================================================
    # Sense and Act
    # ==================================================

    def sense_and_act(self, percept):

        # No food left
        if not percept["all_food"]:
            return "Up"

        # Generate a fresh plan only if needed
        if not self.plan:

            start = tuple(percept["agent_pos"])

            foods = percept["all_food"]

            walls = set(percept["walls"])

            width, height = percept["grid_size"]

            # Closest food using Manhattan distance
            target_food = min(
                foods,
                key=lambda food:
                self.manhattan_distance(
                    start,
                    food
                )
            )

            goals = {target_food}

            # DFS
            if self.active_algo == "DFS":

                self.plan = self.dfs_search(
                    start,
                    goals,
                    walls,
                    width,
                    height
                )

            # UCS
            elif self.active_algo == "UCS":

                self.plan = self.ucs_search(
                    start,
                    goals,
                    walls,
                    width,
                    height
                )

            # A*
            elif self.active_algo == "AStar":

                self.plan = self.astar_search(
                    start_pos=start,
                    goal_pos=target_food,
                    walls=walls,
                    grid_size=(width, height),
                    heuristic_type="manhattan"
                )

            # BFS
            else:

                self.plan = self.bfs_search(
                    start,
                    goals,
                    walls,
                    width,
                    height
                )

        # Execute next action
        if self.plan:
            return self.plan.pop(0)

        return "Up"


# ==================================================
# Test
# ==================================================

if __name__ == "__main__":

    agent = SearchAgent()

    start = (0, 0)
    goal = (3, 4)

    print(
        "Manhattan:",
        agent.manhattan_distance(start, goal)
    )

    print(
        "Euclidean:",
        agent.euclidean_distance(start, goal)
    )

    path = agent.astar_search(
        start_pos=start,
        goal_pos=goal,
        walls=set(),
        grid_size=(10, 10),
        heuristic_type="manhattan"
    )

    print("A* Path:", path)
    print("Path Length:", len(path))