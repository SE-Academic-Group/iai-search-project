import tkinter as tk

# Constants
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
TITLE="project 1: Robot finds the way".upper()
COURSE_NAME="Course: Introduction to Artificial Intelligence"
favicon_path = "favicon.ico"
window_title = "CSC14003 - Introduction to Artificial Intelligence - Search Project"

root = tk.Tk()
root.title(window_title)
root.iconbitmap(favicon_path)
root.resizable(False, False)
root.configure(bg='white')

# Left Frame - Information
left_frame = tk.Frame(root, pady=20, padx=20, bg='lightgreen')
left_frame.pack(side=tk.LEFT, fill=tk.BOTH)

def draw_hr():
    hr = tk.Label(left_frame, text=['=========================================================='], bg='lightgreen')
    hr.pack(pady=(0, 8))

left_label = tk.Label(left_frame, text="Project Information", font=('Dank Mono', 12, 'bold'))
left_label.pack(pady=(0, 20))

title = tk.Label(left_frame, text=TITLE, font=('Times New Roman', 16, 'bold'))
title.pack(pady=(0, 28))

course_name = tk.Label(left_frame, text=COURSE_NAME, font=('Dank Mono', 12, 'bold'), anchor='w', justify='left')
course_name.pack(pady=(0, 12), fill=tk.X)

draw_hr()

students_info = tk.Label(left_frame, text="Group members information:", font=('Dank Mono', 14, 'bold'))
students_info.pack(pady=(0, 8), fill=tk.X)

for i, member in enumerate(GROUP_MEMBERS):
    student = tk.Label(left_frame, text=member, font=('Dank Mono', 10, 'bold'))
    student.pack(pady=(0, 8), fill=tk.X)

draw_hr()

tk.Label(left_frame, text='Please select a search algorithm', font=('Dank Mono', 12, 'bold')).pack(pady=(0, 12), fill=tk.X)
for i, alg in enumerate(ALGORITHMS):
    alg_radio = tk.Radiobutton(left_frame, text=alg, value=alg, font=('Dank Mono', 10, 'bold'))
    alg_radio.pack(pady=(0, 8), fill=tk.X)

draw_hr()
tk.Label(left_frame, text='Result:', font=('Dank Mono', 12, 'bold')).pack(pady=(0, 12), fill=tk.X)


# Right Frame - Search Performance
right_frame = tk.Frame(root, pady=20, padx=20, bg='white')
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

right_label = tk.Label(right_frame, text="Search Performance", font=('Arial 16'))
right_label.pack(pady=(0, 20), side=tk.TOP, fill=tk.X, expand=True)


root.mainloop()