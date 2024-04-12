from tkinter import *
from time import sleep
from scipy.spatial import ConvexHull
from queue import Queue
from queue import PriorityQueue
from itertools import permutations

GROUP_MEMBERS = [
    "21120502 - Tran Duc Minh",
    "21120515 - Tran Phuoc Nhan",
    "21120521 - Nguyen Phuc Phat",
    "21120524 - Truong Minh Phat",
]
ALGORITHMS = [
    "BFS - Breadth First Search",
    "GBFS - Greedy Best First Search",
    "A* - A Star Search",
    "A* Search With Checkpoints"
]
TITLE = "project 1: Robot finds the path".upper()
MATRIX_CODE = {
    "start": 0,
    "goal": 1,
    "obstacle": 2,
    "obstacle_vertex": 3,
    "empty": 4,
    "visited": 5,
    "path": 6,
    "edge": 7,
    "checkpoint": 8
}
BLOCK_LIST = [
    MATRIX_CODE["obstacle"],
    MATRIX_CODE["obstacle_vertex"],
    MATRIX_CODE['edge']
    ]
MATRIX_CODE_COLORS = {
    "start": "#0ea5e9",
    "goal": "orangered",
    "obstacle": "#94a3b8",
    "obstacle_vertex": "#64748b",
    "empty": "white",
    "visited": "lightblue",
    "path": "lightgreen",
    "edge": "lightgrey",
    "checkpoint": "yellow"
}
FAVICON_PATH = "favicon.ico"
WINDOW_TITLE = "CSC14003 - Introduction to Artificial Intelligence - Search Project"
SEARCH_BOARD_SIZE = 550
INPUT_FILE_PATH = "input.txt"

root = Tk()
root.title(WINDOW_TITLE)
root.iconbitmap(FAVICON_PATH)
root.geometry("+0+0")
root.resizable(False, False)
root.configure(bg="white")

def bresenham(x0, y0, x1, y1):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    err = dx - dy
    # points = [(x0, y0)]
    points = []
    while x0 != x1 or y0 != y1:
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
        points.append((x0, y0))
    points.pop(len(points) - 1)
    return points

class SearchBoard:
    def __init__(self, canvas) -> None:
        self.canvas = canvas
        self.matrix = [[]]

    def setCellValue(self, x: int, y: int, value: int) -> None:
        if (self.matrix[y][x] == MATRIX_CODE['empty'] or self.matrix[y][x] == MATRIX_CODE['visited']):
            self.matrix[y][x] = value

    def read_input_file(self, file_path) -> None:
        with open(file_path, "r") as file:
            n, m = map(int, file.readline().split(","))
            m += 1
            n += 1
            self.m, self.n = m, n
            self.matrix = [[MATRIX_CODE["empty"]] * n for _ in range(m)]
            self.cell_size = SEARCH_BOARD_SIZE // max(m + 1, n + 1)

            # Read all points from one line (the order is start, goal, and checkpoints)
            points = list(map(int, file.readline().split(",")))
            sx, sy, gx, gy = points[:4]
            self.setCellValue(sx, sy, MATRIX_CODE["start"])
            self.setCellValue(gx, gy, MATRIX_CODE["goal"])
            self.start_point = (sx, sy)
            self.goal_point = (gx, gy)

            self.checkpoints = [(points[i], points[i + 1]) for i in range(4, len(points), 2)]
            for x, y in self.checkpoints:
                self.setCellValue(x, y, MATRIX_CODE["checkpoint"])

            for i in range(n):
                self.setCellValue(i, 0, MATRIX_CODE["edge"])
                self.setCellValue(i, m - 1, MATRIX_CODE["edge"])

            for i in range(m):
                self.setCellValue(0, i, MATRIX_CODE["edge"])
                self.setCellValue(n - 1, i, MATRIX_CODE["edge"])

            no_obstacles = int(file.readline())

            for _ in range(no_obstacles):
                coors = list(map(int, file.readline().split(",")))
                no_points = len(coors) // 2
                coors_points = []

                for i in range(0, no_points * 2, 2):
                    x, y = min(coors[i], n - 1), min(coors[i + 1], m - 1)
                    coors_points.append((x, y))

                hull = ConvexHull(coors_points)
                hull_point_indices = hull.vertices
                convex_hull_points = [coors_points[i] for i in hull_point_indices]

                self.set_obstacle_points(convex_hull_points)

    def set_obstacle_points(self, points: list[tuple[int, int]]) -> None:
        length = len(points)

        for x, y in points:
            self.setCellValue(x, y, MATRIX_CODE["obstacle_vertex"])

        for i in range(length):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % length]
            line_points = bresenham(x1, y1, x2, y2)

            for point in line_points:
                self.setCellValue(point[0], point[1], MATRIX_CODE["obstacle"])

    def draw_search_board(self) -> None:
        canvas, matrix = self.canvas, self.matrix
        m, n = self.m, self.n

        canvas.delete("all")

        cell_size = self.cell_size
        offset = 0

        for i in range(m):
            canvas.create_text(offset, (i + 1.5) * cell_size, text=f" {i}", anchor="w")
        for j in range(n):
            canvas.create_text((j + 1.5) * cell_size, offset, text=f" {j}", anchor="n")

        for i in range(m):
            for j in range(n):
                code = matrix[i][j]
                color = MATRIX_CODE_COLORS[
                    list(MATRIX_CODE.keys())[list(MATRIX_CODE.values()).index(code)]
                ]

                canvas.create_rectangle(
                    (j + 1) * cell_size,
                    (i + 1) * cell_size,
                    (j + 2) * cell_size,
                    (i + 2) * cell_size,
                    fill=color,
                    outline="black",
                )

        root.update_idletasks()

    def start(self) -> None:
        self.read_input_file(INPUT_FILE_PATH)
        self.canvas.after(0, self.draw_search_board())

    # Check if a cell is within the table
    def isInTable(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.m
    def is_valid_point(self, point):
        x = point[0]
        y = point[1]
        if(x < 0 or x > self.n) or (y < 0 or y > self.m):
            return False
        return True
    def is_move_point(self, point):
        x = point[0]
        y = point[1]
        if self.is_valid_point(point):
            if(self.matrix[y][x] == MATRIX_CODE["empty"] or self.matrix[y][x] == MATRIX_CODE["goal"] or self.matrix[y][x] == MATRIX_CODE["start"] or self.matrix[y][x] == MATRIX_CODE["checkpoint"] or self.matrix[y][x] == MATRIX_CODE["visited"] or self.matrix[y][x] == MATRIX_CODE["path"]):
                return True
        return False
    def get_vertex_neighbours(self, point):
        n = []
        for dx, dy in [(1,0),(-1,0),(0, 1),(0, -1)]:
            new_point = (point[0] + dx, point[1] + dy)
            if(self.is_move_point(new_point)):
                n.append(new_point)
        return n
    def bfs(self) -> None:
        # Directions for movement: right, left, up, down, and diagonals
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        queue = Queue()  # Queue for BFS
        visited = set()  # Keep track of visited cells
        parent = {}  # To reconstruct the path

        start_x, start_y = self.start_point
        goal_x, goal_y = self.goal_point

        cost = 0
        # Enqueue start point and mark as visited
        queue.put((start_x, start_y, cost))
        visited.add((start_x, start_y))
        parent[(start_x, start_y)] = None  # Start point has no parent
        # Variable to check if goal is reached
        found_goal = False

        # BFS algorithm
        while not queue.empty() and not found_goal:
            x, y, cost = queue.get()

            for dx, dy in directions:
                # Next cell
                nx, ny = x + dx, y + dy
                # Check if the next cell is within the table and has not been visited
                if self.isInTable(nx, ny) and (nx, ny) not in visited:
                    # Check if the next cell is not an obstacle
                    if self.matrix[ny][nx] not in BLOCK_LIST:
                        queue.put((nx, ny, cost + 1))   # Enqueue next cell
                        visited.add((nx, ny)) # Mark next cell as visited
                        parent[(nx, ny)] = (x, y)  # Mark current cell as parent

                        # # Visualize progress
                        self.draw_progress([(nx, ny)])

                        # Check if goal is reached
                        if (nx, ny) == (goal_x, goal_y):
                            found_goal = True
                            cost += 1
                            break

        if found_goal:
            # Reconstruct path
            path = []
            current = (goal_x, goal_y)
            while current:
                path.append(current)
                current = parent[current]
            path.reverse()
            return (path, cost, len(visited))

        return (None, None, None)

    # Heuristic function for Greedy Best First Search
    def heuristic(self,a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

    # Greedy Best First Search
    def gbfs(self) -> None:
        # Initialize variables
        goal_x, goal_y = self.goal_point
        start_x, start_y = self.start_point
        visited = set()
        queue = PriorityQueue()
        queue.put((0, (start_x, start_y)))  # Priority queue uses heuristic as the first item
        parent = {(start_x, start_y): None}  # To reconstruct the path

        # Directions for movement: right, left, up, down, and diagonals
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        # GBFS algorithm
        while not queue.empty():
            # Get the node with the lowest heuristic value
            (current_x, current_y) = queue.get()[1]

            # Check if goal is reached
            if (current_x, current_y) == (goal_x, goal_y):
                break

            # Skip if the node has been visited
            if (current_x, current_y) in visited:
                continue

            # Mark the node as visited
            visited.add((current_x, current_y))
            self.draw_progress([(current_x, current_y)]) # Visualize progress

            for dx, dy in directions:
                # The next cell
                n_x, n_y = current_x + dx, current_y + dy
                # Check if the next cell is within the table and has not been visited
                if self.isInTable(n_x, n_y) and (n_x, n_y) not in visited:
                    # Check if the next cell is not an obstacle
                    if self.matrix[n_y][n_x] not in BLOCK_LIST:
                        next_node = (n_x, n_y)
                        priority = self.heuristic(next_node, (goal_x, goal_y))
                        queue.put((priority, next_node))
                        parent[next_node] = (current_x, current_y)

        # Reconstruct path
        path = []
        current = (goal_x, goal_y)
        while current in parent:
            path.append(current)
            current = parent[current]
        path.reverse()

        # Return path, cost, and number of visited nodes
        if path:
            return (path, len(path) - 1, len(visited))
        else:
            return (None, None, None)

    def a_star(self):
        G = {}
        F = {}

        #Initialize starting values
        G[self.start_point] = 0
        F[self.start_point] = self.heuristic(self.start_point, self.goal_point)

        closedVertices = set()
        openVertices = set([self.start_point])
        cameFrom = {}

        while len(openVertices) > 0:
            #Get the vertex in the open list with the lowest F score
            current = None
            currentFscore = None
            for pos in openVertices:
                if current is None or F[pos] < currentFscore:
                    currentFscore = F[pos]
                    current = pos

            #Check if we have reached the goal
            if current == self.goal_point:
                #Retrace our route backward
                path = [current]
                while current in cameFrom:
                    current = cameFrom[current]
                    path.append(current)
                path.reverse()
                return path, len(path) - 1, len(closedVertices) 

            #Mark the current vertex as closed
            openVertices.remove(current)
            self.draw_progress([(current[0], current[1])])
            closedVertices.add(current)

            #Update scores for vertices near the current point
            for neighbour in self.get_vertex_neighbours(current):
                if neighbour in closedVertices:
                    continue #We have already processed this node exhaustively
                candidateG = G[current] + 1
                candidateH = self.heuristic(neighbour, self.goal_point)
                candidateF = candidateG + candidateH
                if neighbour not in openVertices:
                    openVertices.add(neighbour) #Discovered a new vertex
                elif candidateF >= F[neighbour]:
                    continue 

                cameFrom[neighbour] = current
                G[neighbour] = candidateG
                H = self.heuristic(neighbour, self.goal_point)
                F[neighbour] = G[neighbour] + H

        return None, None, None

    def a_star_alternative(self, start_point, goal_point):
        G = {}
        F = {}

        # Initialize starting values
        G[start_point] = 0
        F[start_point] = self.heuristic(start_point, goal_point)

        closedVertices = set()
        openVertices = set([start_point])
        cameFrom = {}

        while len(openVertices) > 0:
            # Get the vertex in the open list with the lowest F score
            current = None
            currentFscore = None
            for pos in openVertices:
                if current is None or F[pos] < currentFscore:
                    currentFscore = F[pos]
                    current = pos

            # Check if we have reached the goal
            if current == goal_point:
                # Retrace our route backward
                path = [current]
                while current in cameFrom:
                    current = cameFrom[current]
                    path.append(current)
                path.reverse()
                return path, len(path) - 1, len(closedVertices)

                # Mark the current vertex as closed
            openVertices.remove(current)
            self.draw_progress([(current[0], current[1])])
            closedVertices.add(current)

            # Update scores for vertices near the current point
            for neighbour in self.get_vertex_neighbours(current):
                if neighbour in closedVertices:
                    continue  # We have already processed this node exhaustively
                candidateG = G[current] + 1
                candidateH = self.heuristic(neighbour, goal_point)
                candidateF = candidateG + candidateH
                if neighbour not in openVertices:
                    openVertices.add(neighbour)  # Discovered a new vertex
                elif candidateF >= F[neighbour]:
                    continue

                cameFrom[neighbour] = current
                G[neighbour] = candidateG
                H = self.heuristic(neighbour, goal_point)
                F[neighbour] = G[neighbour] + H

        return None, None, None

    def a_star_with_checkpoints(self):
        checkpoints = self.checkpoints
        points = [self.start_point] + checkpoints + [self.goal_point]
        # Initialize adjacency matrix to store the cost of the path between each pair of points
        adjacency_matrix = [[float('inf') for _ in range(len(points))] for _ in range(len(points))]
        # Initialize path matrix
        path_matrix = [[None for _ in range(len(points))] for _ in range(len(points))]

        total_visited = 0
        # Calculate the cost of the path from each pair of points
        for i in range(len(points)-1):
            for j in range(i + 1, len(points)):
                # Skip finding the path between the start and goal points
                if i == 0 and j == len(points) - 1:
                    continue

                path, cost, visited = self.a_star_alternative(points[i], points[j])
                if path is None:
                    return None, None, None
                self.start()
                search_board.canvas.after(0, search_board.draw_path(path))

                total_visited += visited
                adjacency_matrix[i][j] = adjacency_matrix[j][i] = cost
                path_matrix[i][j] = path
                path_matrix[j][i] = path[::-1]

        # Adjusting the adjacency matrix: cost from all checkpoints to the start is infinity, and cost from goal to all checkpoints is infinity
        for i in range(1, len(points) - 1):
            adjacency_matrix[i][0] = float('inf')
            adjacency_matrix[-1][i] = float('inf')
        adjacency_matrix[-1][0] = 0

        # Solve the Traveling Salesman Problem using dynamic programming
        class TSP:
            def __init__(self):
                self.optimal_path = []
                self.optimal_cost = float('inf')
                self.visited_points = [False] * len(points)
                self.checkpoints = checkpoints

                self.current_path = [0] * len(points)
                self.visited_points[0] = True
            def solve_tsp(self):
                checkpoint_indexes = [i for i in range(1, len(points) - 1)]
                for perm in permutations(checkpoint_indexes):
                    current_cost = 0
                    current = 0
                    for i in range(len(perm)):
                        current_cost += adjacency_matrix[current][perm[i]]
                        current = perm[i]
                    current_cost += adjacency_matrix[current][-1]
                    if current_cost < self.optimal_cost:
                        self.optimal_cost = current_cost
                        self.optimal_path = [0] + list(perm) + [len(points) - 1]

        tsp = TSP()
        tsp.solve_tsp()
        path = tsp.optimal_path
        cost = tsp.optimal_cost
        # Get the final path
        final_path = []
        for i in range(len(path)-1):
            final_path += path_matrix[path[i]][path[i + 1]]
        return final_path, cost, total_visited

    def draw_progress(self, progress: list[tuple[int, int]]) -> None:
        for x, y in progress:
            self.setCellValue(x, y, MATRIX_CODE["visited"])
            self.canvas.after(0, self.draw_search_board())

    def draw_path(self, path: list[tuple[int, int]]) -> None:
        cell_size = self.cell_size

        for x, y in path:
            self.setCellValue(x, y, MATRIX_CODE["path"])
            self.canvas.after(0, self.draw_search_board())

        line_path = [self.start_point] + path + [self.goal_point]

        for i in range(len(line_path) - 1):
            x1, y1 = line_path[i]
            x2, y2 = line_path[i + 1]

            self.canvas.create_line(
                (x1 + 1) * cell_size + cell_size // 2,
                (y1 + 1) * cell_size + cell_size // 2,
                (x2 + 1) * cell_size + cell_size // 2,
                (y2 + 1) * cell_size + cell_size // 2,
                fill='darkgreen',
                width=3
            )


def start_algorithm():
    algo_map = {
        0: search_board.bfs,
        1: search_board.gbfs,
        2: search_board.a_star,
        3: search_board.a_star_with_checkpoints
    }

    algo_func = algo_map[selected_alg_idx.get()]

    search_board.start()
    (path, cost, visited) = algo_func()

    result.pack(pady=(20, 8))

    if path is None:
        no_path_label.pack()
        return

    search_board.canvas.after(0, search_board.draw_path(path))

    cost_label.config(text=f"Cost of the path: {cost}")
    visited_label.config(text=f"Number of visited nodes: {visited}")
    cost_label.pack(pady=(0, 8))
    visited_label.pack(pady=(0, 8))


def on_alg_selected():
    search_board.start()
    result.forget()
    cost_label.forget()
    visited_label.forget()
    no_path_label.forget()


# Global Variables
selected_alg_idx = IntVar()
left_frame = Frame(root, pady=20, padx=20, bg="lightgreen")
right_frame = Frame(root, pady=20, padx=40, bg="white")
result = Label(left_frame, text="Result", font="arial 14")
cost_label = Label(left_frame, text="Cost: ", font="arial 12")
visited_label = Label(left_frame, text="Visited: ", font="arial 12")
alg_name_label = Label(left_frame, text="Algorithm: ", font="arial 12")
no_path_label = Label(left_frame, text="No path found", font="arial 12", foreground="red")
search_board_canvas = Canvas(
    right_frame,
    bg="white",
    width=SEARCH_BOARD_SIZE,
    height=SEARCH_BOARD_SIZE,
    bd=0,
    highlightthickness=0,
    relief="ridge",
)
search_board = SearchBoard(search_board_canvas)

# Left Frame - Information
left_frame.pack(side=LEFT, fill=BOTH)

Label(left_frame, text="Project Information", font=("Dank Mono", 12, "bold")).pack(
    pady=(0, 20)
)
Label(left_frame, text=TITLE, font=("Times New Roman", 16, "bold")).pack(pady=(0, 28))
Label(left_frame, text="Group members information:", font="arial 14").pack(
    pady=(0, 8), fill=X
)

for i, member in enumerate(GROUP_MEMBERS):
    Label(left_frame, text=member, font="arial 12").pack(pady=(0, 8), fill=X)

Label(left_frame, text="Please edit input.txt to change \nthe data of the search board", font="arial 12").pack(
    pady=(24, 12), fill=X
)

Label(left_frame, text="Please select a search algorithm", font="arial 14").pack(
    pady=(12, 12), fill=X
)

for i, alg in enumerate(ALGORITHMS):
    alg_radio = Radiobutton(
        left_frame,
        text=alg,
        value=i,
        font="arial 12",
        activebackground="lightblue",
        variable=selected_alg_idx,
        command=on_alg_selected,
    )
    alg_radio.pack(pady=(0, 8), fill=X)

    if i == 0:
        alg_radio.select()

# Right Frame - Search Performance
right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

Label(right_frame, text="Search Performance", font=("Dank Mono", 12, "bold")).pack(
    pady=(0, 8)
)

annotation_frame = Frame(right_frame, bg="white")
annotations = [
    ("Start", MATRIX_CODE_COLORS['start'], 'white'),
    ("Goal", MATRIX_CODE_COLORS['goal'], 'white'),
    ("Obstacle", MATRIX_CODE_COLORS['obstacle'], None),
    ("Obstacle Vertex", MATRIX_CODE_COLORS['obstacle_vertex'], 'white'),
    ("Visited", MATRIX_CODE_COLORS['visited'], None),
    ("Path", MATRIX_CODE_COLORS['path'], None)
]

for i, (text, bg, foreground) in enumerate(annotations):
    Label(annotation_frame, text=text, bg=bg, foreground=foreground).grid(
        row=0, column=i, padx=(0, 8), pady=(0, 4)
    )
annotation_frame.pack(pady=12)

search_board_canvas.pack()
start_button = Button(
    right_frame,
    text="Find the path",
    font="arial 12",
    command=start_algorithm,
    activebackground="lightblue",
)
start_button.pack(pady=(8, 0))

search_board.start()

root.mainloop()
