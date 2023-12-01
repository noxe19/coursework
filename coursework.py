"""
переделать отоброжение дамок
прописать ходы дамок
написать интерфейс
написать окна регистрации\авторизации
"""


from tkinter import *

click1 = [0, 0]
click2 = [0, 0]
click_buf = 0
click_stop = False
player_move = True
move_count = 0
users = ["white", "red"]
queue = "white"


canvases = [
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0]
]

board_checkers = [
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 3, 0, 3, 0, 3, 0],
    [0, 3, 0, 3, 0, 3, 0, 3],
    [3, 0, 3, 0, 3, 0, 3, 0]
]


def register_login():
    pass


def board_rendering():
    board_canvas.delete("all")
    print(board_checkers)
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 1:
                board_canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill="black", outline="black")
                if board_checkers[i][j] == 2:
                    board_canvas.create_oval(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill="red", outline="black")
                if board_checkers[i][j] == 3:
                    board_canvas.create_oval(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill="white", outline="black")
                if board_checkers[i][j] == 12:
                    board_canvas.create_oval(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill="red", outline="black")
                    board_canvas.create_oval(j * 51.5, i * 51.5, (j + 0.8) * 50, (i + 0.8) * 50, fill="yellow", outline="black")
                if board_checkers[i][j] == 13:
                    board_canvas.create_oval(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill="white", outline="black")
                    board_canvas.create_oval(j * 57.5, i * 57.5, (j + 1) * 45, (i + 1) * 45, fill="yellow", outline="black")


def click(event):
    x = event.x // 50
    y = event.y // 50
    if player_move:
        turn_player_click(x, y)
    else:
        minimax(x, y)


def turn_player_click(x, y):
    global click_stop
    global move_count
    global player_move
    global board_checkers
    global click_buf
    global click1
    global click2
    if move_count < 2:
        if board_checkers[y][x] != 2:
            if board_checkers[y][x] == 3:
                if click_buf == 1:
                    click1[0] = x
                    click1[1] = y
                click1[0] = x
                click1[1] = y
                click_buf = 1
                click_stop = False
                print("взял")
            elif board_checkers[y][x] == 0:
                if not click_stop:
                    if canvases[y][x] == 1:
                        click2[0] = x
                        click2[1] = y
                        click_buf = 0
                        killed_checker(x, y)
                        print("ходит")
                    else:
                        print("нельзя")
        else:
            print("чужая")


def move_checker(x, y):
    global click_stop
    global player_move
    global move_count
    global board_checkers
    global click1

    if player_move:
        board_checkers[click2[1]][click2[0]] = board_checkers[click1[1]][click1[0]]
        board_checkers[click1[1]][click1[0]] = 0
        become_queen()
    else:
        board_checkers[click2[1]][click2[0]] = board_checkers[click1[1]][click1[0]]
        board_checkers[click1[1]][click1[0]] = 0
        become_queen()
    if move_count == 2:
        if player_move:
            player_move = False
            print("ход красных")
        else:
            player_move = True
            print("ход белых")
        move_count = 0
    click_stop = True
    board_rendering()


def board():
    global game_window
    game_window = Tk()
    game_window.title("Двухходовые шашки – Поддавки")
    game_window.geometry('401x401+100+100')
    global board_canvas
    board_canvas = Canvas(game_window, bg="white", width=400, height=400)
    board_canvas.bind("<Button-1>", click)
    board_canvas.pack()
    board_rendering()
    mainloop()


def killed_checker(x, y):
    global click1
    global click2
    global move_count
    global board_checkers
    buf = False
    if board_checkers[y][x] == 0:
        if abs(click1[0] - click2[0]) == abs(click1[1] - click2[1]) == 2:
            if click1[0] - click2[0] == 2 and click1[1] - click2[1] == 2:
                if player_move:
                    if board_checkers[y + 1][x + 1] != 3:
                        board_checkers[y + 1][x + 1] = 0
                        buf = True
                    else:
                        print("нельзя")
                else:
                    if board_checkers[y + 1][x + 1] != 2:
                        board_checkers[y + 1][x + 1] = 0
                        buf = True
                    else:
                        print("нельзя")
            elif click1[0] - click2[0] == 2 and click1[1] - click2[1] == -2:
                if player_move:
                    if board_checkers[y - 1][x + 1] != 3:
                        board_checkers[y - 1][x + 1] = 0
                        buf = True
                    else:
                        print("нельзя")
                else:
                    if board_checkers[y - 1][x + 1] != 2:
                        board_checkers[y - 1][x + 1] = 0
                        buf = True
                    else:
                        print("нельзя")
            elif click1[0] - click2[0] == -2 and click1[1] - click2[1] == -2:
                if player_move:
                    if board_checkers[y - 1][x - 1] != 3:
                        board_checkers[y - 1][x - 1] = 0
                        buf = True
                    else:
                        print("нельзя")
                else:
                    if board_checkers[y - 1][x - 1] != 2:
                        board_checkers[y - 1][x - 1] = 0
                        buf = True
                    else:
                        print("нельзя")
            elif click1[0] - click2[0] == -2 and click1[1] - click2[1] == 2:
                if player_move:
                    if board_checkers[y + 1][x - 1] != 3:
                        board_checkers[y + 1][x - 1] = 0
                        buf = True
                    else:
                        print("нельзя")
                else:
                    if board_checkers[y + 1][x - 1] != 2:
                        board_checkers[y + 1][x - 1] = 0
                        buf = True
                    else:
                        print("нельзя")
            #if move_count == 0:
            #    move_count += 1
            if buf:
                #if move_count == 0:
                #    move_count += 1
                if player_move:
                    if board_checkers[y-1][x-1] != 2 or board_checkers[y+1][x+1] != 2 or board_checkers[y-1][x+1] != 2 or board_checkers[y+1][x-1] != 2:
                        move_count += 1
                else:
                    if board_checkers[y-1][x-1] != 3 or board_checkers[y+1][x+1] != 3 or board_checkers[y-1][x+1] != 3 or board_checkers[y+1][x-1] != 3:
                        move_count += 1
                move_checker(x, y)

        elif abs(click1[0] - click2[0]) == abs(click1[1] - click2[1]) == 1:
            if player_move:
                if click1[1] - click2[1] == 1:
                    move_count += 1
                    move_checker(x, y)
            else:
                if click1[1] - click2[1] == -1:
                    move_count += 1
                    move_checker(x, y)


def become_queen():
    global board_checkers
    for j in range(1, 8, 2):
        if board_checkers[0][j] == 3:
            board_checkers[0][j] = 13
    for j in range(0, 7, 2):
        if board_checkers[7][j] == 2:
            board_checkers[7][j] = 12


def check_kill():
    mandatory_move = []
    for i in range(8):
        for j in range(8):
            if board_checkers[i][j] == 3:
                if i == 0 and j == 0:
                    if board_checkers[i+1][j+1] == 2:
                        if board_checkers[i+2][j+2] == 0:
                            mandatory_move.append([i, j])
                if i == 0 and j == 7:
                    if board_checkers[i+1][j-1] == 2:
                        if board_checkers[i + 2][j - 2] == 0:
                            mandatory_move.append([i, j])
                if i == 7 and j == 0:
                    if board_checkers[i - 1][j + 1] == 2:
                        if board_checkers[i - 2][j + 2] == 0:
                            mandatory_move.append([i, j])
                if i == 7 and j == 7:
                    if board_checkers[i - 1][j - 1] == 2:
                        if board_checkers[i - 2][j - 2] == 0:
                            mandatory_move.append([i, j])



def minimax(x, y):
    global player_move
    global move_count
    global board_checkers
    global click_stop
    global click_buf
    global click1
    global click2
    if move_count < 2:
        if board_checkers[y][x] != 3:
            if board_checkers[y][x] == 2:
                if click_buf == 1:
                    click1[0] = x
                    click1[1] = y
                click1[0] = x
                click1[1] = y
                click_buf = 1
                print("взял")
                click_stop = False
            elif board_checkers[y][x] == 0:
                if not click_stop:
                    if canvases[y][x] == 1:
                        click2[0] = x
                        click2[1] = y
                        click_buf = 0
                        killed_checker(x, y)
                        print("ходит")
                    else:
                        print("нельзя")
        else:
            print("чужая")

board()
