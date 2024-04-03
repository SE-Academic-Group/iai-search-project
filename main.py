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
        self.archived_matrix = [[]]

    def setCellValue(self, x, y, value) -> None:
        self.matrix[y][x] = value

    def read_input_file(self, file_path) -> None:
        with open(file_path, "r") as file:
            m, n = map(int, file.readline().split(","))
            self.m, self.n = m, n
            self.matrix = [[MATRIX_CODE["empty"]] * n for _ in range(m)]

            sx, sy, gx, gy = map(int, file.readline().split(","))
            self.setCellValue(sx, sy, MATRIX_CODE["start"])
            self.setCellValue(gx, gy, MATRIX_CODE["goal"])

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

            self.archived_matrix = self.matrix

    def draw_obstacle_from_points(self, points) -> None:
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



    def draw_search_board(self):
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

                if code == MATRIX_CODE["start"]:
                    color = "#0ea5e9"
                elif code == MATRIX_CODE["goal"]:
                    color = "orangered"
                elif code == MATRIX_CODE["obstacle"]:
                    color = "lightgrey"
                elif code == MATRIX_CODE["obstacle_vertex"]:
                    color = "grey"
                elif code == MATRIX_CODE["visited"]:
                    color = "lightblue"
                else:
                    color = "white"

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

    def start(self):
        self.read_input_file(INPUT_FILE_PATH)
        self.draw_search_board()

    def dfs():
        pass

    def gbfs():
        pass

    def a_star():
        pass

    def draw_progress():
        pass

    def draw_path():
        pass

def draw_search_board(matrix):
    canvas = search_board_canvas
    canvas.delete("all")
    m, n = len(matrix), len(matrix[0])
    cell_size = SEARCH_BOARD_SIZE // max(m + 1, n + 1)

    for i in range(m):
        canvas.create_text(6, (i + 1.5) * cell_size, text=f" {i}", anchor="w")
    for j in range(n):
        canvas.create_text((j + 1.5) * cell_size, 6, text=f" {j}", anchor="n")

    for i in range(m):
        for j in range(n):
            code = matrix[i][j]

            if code == MATRIX_CODE["start"]:
                color = "#0ea5e9"
            elif code == MATRIX_CODE["goal"]:
                color = "orangered"
            elif code == MATRIX_CODE["obstacle"]:
                color = "lightgrey"
            elif code == MATRIX_CODE["visited"]:
                color = "lightblue"
            else:
                color = "white"

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

def start_algorithm():
    pass

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
    pady=(0, 20)
)

search_board_canvas.pack()
start_button = Button(
    right_frame,
    text="Find the path",
    font="arial 12",
    command=start_algorithm,
    activebackground="lightblue",
)
start_button.pack(pady=(20, 0))

search_board.start()

root.mainloop()
