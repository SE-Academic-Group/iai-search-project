from tkinter import *
from time import sleep
from scipy.spatial import ConvexHull
from queue import Queue
from queue import PriorityQueue

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
}
MATRIX_CODE_COLORS = {
    "start": "#0ea5e9",
    "goal": "orangered",
    "obstacle": "lightgrey",
    "obstacle_vertex": "grey",
    "empty": "white",
    "visited": "lightblue",
    "path": "lightgreen"
}
FAVICON_PATH = "favicon.ico"
WINDOW_TITLE = "CSC14003 - Introduction to Artificial Intelligence - Search Project"
SEARCH_BOARD_SIZE = 600
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
            self.m, self.n = m, n
            self.matrix = [[MATRIX_CODE["empty"]] * n for _ in range(m)]

            sx, sy, gx, gy = map(int, file.readline().split(","))
            self.setCellValue(sx, sy, MATRIX_CODE["start"])
            self.setCellValue(gx, gy, MATRIX_CODE["goal"])
            self.start_point = (sx, sy)
            self.goal_point = (gx, gy)

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

                self.draw_obstacle_from_points(convex_hull_points)

    def draw_obstacle_from_points(self, points: list[tuple[int, int]]) -> None:
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

        cell_size = SEARCH_BOARD_SIZE // max(m + 1, n + 1)
        offset = 6

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

                i = i + 1
                j = j + 1
                canvas.create_rectangle(
                    j * cell_size,
                    i * cell_size,
                    (j + 1) * cell_size,
                    (i + 1) * cell_size,
                    fill=color,
                    outline="black",
                )
                i = i - 1
                j = j - 1

        root.update_idletasks()

    def start(self) -> None:
        self.read_input_file(INPUT_FILE_PATH)
        self.draw_search_board()

    # Check if a cell is within the table
    def isInTable(self, x, y):
        return 0 <= x < self.n and 0 <= y < self.m

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
                    if self.matrix[ny][nx] not in [MATRIX_CODE["obstacle"], MATRIX_CODE["obstacle_vertex"]]:
                        queue.put((nx, ny, cost + 1))   # Enqueue next cell
                        visited.add((nx, ny)) # Mark next cell as visited
                        parent[(nx, ny)] = (x, y)  # Mark current cell as parent

                        # Visualize progress
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

        # Return path, cost, and number of visited nodes
        if path:
            return (path, cost, len(visited))
        else:
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
                    if self.matrix[n_y][n_x] not in [MATRIX_CODE["obstacle"], MATRIX_CODE["obstacle_vertex"]]:
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

    def a_star() -> None:
        pass

    def draw_progress(self, progress: list[tuple[int, int]]) -> None:
        for x, y in progress:
            self.setCellValue(x, y, MATRIX_CODE["visited"])
            self.draw_search_board()

    def draw_path(self, path: list[tuple[int, int]]) -> None:
        for x, y in path:
            self.setCellValue(x, y, MATRIX_CODE["path"])
            self.draw_search_board()

        cell_size = SEARCH_BOARD_SIZE // max(self.m + 1, self.n + 1)

        line_path = [self.start_point] + path + [self.goal_point]

        for i in range(len(line_path) - 1):
            x1, y1 = line_path[i]
            x2, y2 = line_path[i + 1]

            self.canvas.create_line(
                (x1 + 1) * cell_size + cell_size // 2,
                (y1 + 1) * cell_size + cell_size // 2,
                (x2 + 1) * cell_size + cell_size // 2,
                (y2 + 1) * cell_size + cell_size // 2,
                fill=MATRIX_CODE_COLORS['goal'],
                width=3
            )


def start_algorithm():
    algo_map = {
        0: search_board.bfs,
        1: search_board.gbfs,
        2: search_board.a_star
    }

    algo_func = algo_map[selected_alg_idx.get()]

    search_board.start()
    (path, cost, visited) = algo_func();

    search_board.canvas.after(100, search_board.draw_path(path))

    if path is None:
        no_path_label.pack(pady=(20, 8))
        return

    result.pack(pady=(20, 8))
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
no_path_label = Label(left_frame, text="No path found", font="arial 12")
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

Label(left_frame, text="Please select a search algorithm", font="arial 14").pack(
    pady=(24, 12), fill=X
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
