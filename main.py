from tkinter import *
from time import sleep
from scipy.spatial import ConvexHull

GROUP_MEMBERS = [
    "21120502 - Tran Duc Minh",
    "21120515 - Tran Phuoc Nhan",
    "21120521 - Nguyen Phuc Phat",
    "21120524 - Truong Minh Phat",
]
ALGORITHMS = [
    "DFS - Depth First Search",
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
SEARCH_BOARD_SIZE = 650
INPUT_FILE_PATH = "input.txt"

root = Tk()
root.title(WINDOW_TITLE)
root.iconbitmap(FAVICON_PATH)
root.geometry("+0+0")
root.resizable(False, False)
root.configure(bg="white")

class SearchBoard:
    def __init__(self, canvas) -> None:
        self.canvas = canvas
        self.matrix = [[]]

    def setCellValue(self, x: int, y: int, value: int) -> None:
        self.matrix[y][x] = value

    def read_input_file(self, file_path) -> None:
        with open(file_path, "r") as file:
            m, n = map(int, file.readline().split(","))
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
            dx, dy = max(0, abs(x2 - x1) - 1), max(0, abs(y2 - y1) - 1)

            for j in range(1, max(dx, dy) + 1):
                if (x1 <= x2 and y1 <= y2):
                    x, y = min(x1 + j, x2), min(y1 + j, y2)
                elif (x1 <= x2 and y1 > y2):
                    x, y = min(x1 + j, x2), max(y1 - j, y2)
                elif (x1 > x2 and y1 <= y2):
                    x, y = max(x1 - j, x2), min(y1 + j, y2)
                else:
                    x, y = max(x1 - j, x2), max(y1 - j, y2)

                self.setCellValue(x, y, MATRIX_CODE["obstacle"])

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

    def dfs() -> None:
        pass

    def gbfs() -> None:
        pass

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
    # This is for testing purpose
    path = [
                (3,2), (4,2), (5,3), (6,3), (7,3), (8, 3), (9,3), (10,3),
                (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10),
                (10, 11), (11, 11), (12, 11), (13, 11), (14, 11), (14, 12), (14, 13),
                (14, 14), (14, 15), (14, 16), (15, 16)
        ]

    search_board.start()
    search_board.draw_progress(path)
    search_board.canvas.after(100, search_board.draw_path(path))

    # TODO: Show result (cost of path, number of visited nodes, etc.) after performing the search algorithm

def on_alg_selected():
    print(selected_alg_idx.get())

# Global Variables
selected_alg_idx = IntVar()
left_frame = Frame(root, pady=20, padx=20, bg="lightgreen")
right_frame = Frame(root, pady=20, padx=40, bg="white")
result = Label(left_frame, text="Result", font="arial 14")
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
