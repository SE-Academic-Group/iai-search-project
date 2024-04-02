from tkinter import *
from time import sleep

GROUP_MEMBERS = [
    "21120502 - Tran Duc Minh",
    "21120515 - Tran Phuoc Nhan",
    "21120521 - Nguyen Phuc Phat",
    "21120524 - Truong Minh Phat",
]
ALGORITHMS = [
    "DFS - Depth First Search",
    "BFS - Breadth First Search",
    "UCS - Uniform Cost Search",
    "A* - A Star Search",
]
TITLE = "project 1: Robot finds the path".upper()
MATRIX_CODE = {
    "start": 0,
    "goal": 1,
    "obstacle": 2,
    "empty": 3,
    "visited": 4,
}
FAVICON_PATH = "favicon.ico"
WINDOW_TITLE = "CSC14003 - Introduction to Artificial Intelligence - Search Project"
SEARCH_BOARD_SIZE = 650

root = Tk()
root.title(WINDOW_TITLE)
root.iconbitmap(FAVICON_PATH)
root.geometry("+0+0")
root.resizable(False, False)
root.configure(bg="white")

# Classes
class SearchBoard:
    m = 0
    n = 0
    matrix = []

    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.matrix = [[MATRIX_CODE["empty"]] * n for _ in range(m)]

    def setCellValue(self, x, y, value):
        self.matrix[x][y] = value

class ReadInputFileService:
    @staticmethod
    def read_input_file(file_path):
        with open(file_path, "r") as file:
            m, n = map(int, file.readline().split(","))
            search_board = SearchBoard(m, n)

            sx, sy, gx, gy = map(int, file.readline().split(","))
            search_board.setCellValue(sx, sy, MATRIX_CODE["start"])
            search_board.setCellValue(gx, gy, MATRIX_CODE["goal"])

            no_obstacles = int(file.readline())

            for _ in range(no_obstacles):
                coors = list(map(int, file.readline().split(",")))
                no_points = len(coors) // 2

                for i in range(0, no_points * 2, 2):
                    x, y = min(coors[i], n - 1), min(coors[i + 1], m - 1)
                    search_board.setCellValue(x, y, MATRIX_CODE["obstacle"])

            return search_board


# Functions
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
    # result.pack_forget()
    # result.pack()
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

search_board = ReadInputFileService.read_input_file("input.txt")
draw_search_board(search_board.matrix)

root.mainloop()
