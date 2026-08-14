# agent.py

from collections import deque
import heapq


class SearchAgent:
    """
    Search-based agent supporting BFS, DFS and UCS.
    """

    def __init__(self):

    self.plan = []
    self.active_algo = "BFS"

    def get_neighbors(self, state, walls, width, height):
        """
        Returns valid neighboring states.
        """
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

    def bfs_search(self, start, goals, walls, width, height):
        """
        Breadth First Search (FIFO Queue)
        """

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

    def dfs_search(self, start, goals, walls, width, height):
        """
        Depth First Search (LIFO Stack)
        """

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

    def ucs_search(self, start, goals, walls, width, height):
        """
        Uniform Cost Search
        """

        frontier = []
        heapq.heappush(frontier, (0, start, []))

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

    def sense_and_act(self, percept):

    # If no food left
    if not percept["all_food"]:
        return "Up"

    # Create a new plan only when needed
    if not self.plan:

        start = tuple(percept["agent_pos"])

        foods = percept["all_food"]

        walls = set(percept["walls"])

        width, height = percept["grid_size"]

        # Find closest food using Manhattan distance
        target_food = min(
            foods,
            key=lambda food: abs(food[0] - start[0]) +
                             abs(food[1] - start[1])
        )

        goals = {target_food}

        # Select search algorithm
        if self.active_algo == "DFS":

            self.plan = self.dfs_search(
                start,
                goals,
                walls,
                width,
                height
            )

        elif self.active_algo == "UCS":

            self.plan = self.ucs_search(
                start,
                goals,
                walls,
                width,
                height
            )

        else:  # BFS

            self.plan = self.bfs_search(
                start,
                goals,
                walls,
                width,
                height
            )

    # Execute next step in the plan
    if self.plan:
        return self.plan.pop(0)

    return "Up"