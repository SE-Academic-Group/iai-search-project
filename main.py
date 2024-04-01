from tkinter import *
import time

GROUP_MEMBERS = [
    "21120502 - Tran Duc Minh",
    "21120515 - Tran Phuoc Nhan",
    "21120521 - Nguyen Phuc Phat",
    "21120524 - Truong Minh Phat"
]
ALGORITHMS = [
    'DFS - Depth First Search',
    'BFS - Breadth First Search',
    'UCS - Uniform Cost Search',
    'A* - A Star Search'
]
TITLE="project 1: Robot finds the path".upper()
MATRIX_CODE = {
    'start': 'S',
    'goal': 1,
    'obstacle': 2,
    'empty': 3,
    'visited': 4,
}
FAVICON_PATH = "favicon.ico"
WINDOW_TITLE = "CSC14003 - Introduction to Artificial Intelligence - Search Project"
SEARCH_BOARD_SIZE = 650

root = Tk()
root.title(WINDOW_TITLE)
root.iconbitmap(FAVICON_PATH)
root.geometry("+0+0")
root.resizable(False, False)
root.configure(bg='white')

# Left Frame - Information
left_frame = Frame(root, pady=20, padx=20, bg='lightgreen')
left_frame.pack(side=LEFT, fill=BOTH)

def draw_hr():
    hr = Label(left_frame, text=['====================================================='], bg='lightgreen')
    hr.pack(pady=(0, 8))

Label(left_frame, text="Project Information", font=('Dank Mono', 12, 'bold')).pack(pady=(0, 20))
Label(left_frame, text=TITLE, font=('Times New Roman', 16, 'bold')).pack(pady=(0, 28))

draw_hr()

Label(left_frame, text="Group members information:", font=('arial 14')).pack(pady=(0, 8), fill=X)

for i, member in enumerate(GROUP_MEMBERS):
    Label(left_frame, text=member, font=('arial 12')).pack(pady=(0, 8), fill=X)

draw_hr()

Label(left_frame, text='Please select a search algorithm', font=('arial 14')).pack(pady=(0, 12), fill=X)

selected_alg_idx = IntVar()

def on_alg_selected():
    print(selected_alg_idx.get())

for i, alg in enumerate(ALGORITHMS):
    alg_radio = Radiobutton(left_frame, text=alg, value=i, font=('arial 12'), activebackground='lightblue', variable=selected_alg_idx, command=on_alg_selected)
    alg_radio.pack(pady=(0, 8), fill=X)
    if i == 0:
        alg_radio.select()

draw_hr()

Label(left_frame, text='Result', font=('arial 14')).pack(pady=(0, 12), fill=X)

# Right Frame - Search Performance
right_frame = Frame(root, pady=20, padx=40, bg='white')
right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

def draw_search_board(canvas, matrix):
    canvas.delete('all')
    m, n = len(matrix), len(matrix[0])
    cell_size = SEARCH_BOARD_SIZE // max(m + 1, n + 1)

    # draw column index
    for i in range(m):
        canvas.create_text(6, (i + 1.5) * cell_size, text=f' {i}', anchor='w')
    for j in range(n):
        canvas.create_text((j + 1.5) * cell_size, 6, text=f' {j}', anchor='n')

    for i in range(m):
        for j in range(n):
            code = matrix[i][j]
            if code == MATRIX_CODE['start']:
                color = 'yellow'
            elif code == MATRIX_CODE['goal']:
                color = 'red'
            elif code == MATRIX_CODE['obstacle']:
                color = 'black'
            elif code == MATRIX_CODE['visited']:
                color = 'lightblue'
            else:
                color = 'white'
            i = i + 1
            j = j + 1
            canvas.create_rectangle(j * cell_size, i * cell_size, (j + 1) * cell_size, (i + 1) * cell_size, fill=color, outline='black')
            i = i - 1
            j = j - 1

    root.update_idletasks()

Label(right_frame, text="Search Performance", font=('Dank Mono', 12, 'bold')).pack(pady=(0, 20))
search_board_canvas = Canvas(right_frame, bg='white', width=SEARCH_BOARD_SIZE, height=SEARCH_BOARD_SIZE,  bd=0, highlightthickness=0, relief='ridge')
search_board_canvas.pack()

m, n = 10, 10
matrices = [
    [
    [MATRIX_CODE['start'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['goal'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']]
    ],
    [
    [MATRIX_CODE['start'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['visited'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['goal'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']]
    ],
    [
    [MATRIX_CODE['start'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['visited'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['visited'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['goal'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']]
    ],
    [
    [MATRIX_CODE['start'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['visited'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['visited'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['visited'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['goal'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']],
    [MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty'],MATRIX_CODE['empty']]
    ]
]
draw_search_board(search_board_canvas, matrices[0])

def start_algorithm():
    for matrix in matrices:
        draw_search_board(search_board_canvas, matrix)
        time.sleep(0.2)

start_button = Button(right_frame, text="Find the path", font=('arial 12'), command=start_algorithm, activebackground='lightblue')
start_button.pack(pady=(20, 0))


root.mainloop()
