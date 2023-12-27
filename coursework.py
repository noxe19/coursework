from tkinter import *
import json
import copy
import os
from random import randint


click1 = [0, 0]
click2 = [0, 0]
click_buf = 0
player_move = 3
move_count = 0
click_stop = True
shift_amount = 3

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

board_checkers_start = [
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [3, 0, 3, 0, 3, 0, 3, 0],
    [0, 3, 0, 3, 0, 3, 0, 3],
    [3, 0, 3, 0, 3, 0, 3, 0]
]

board_checkers = copy.deepcopy(board_checkers_start)


def user_file(user_name, password, shift_amount, mode, lab_erorr, main):
    file_path = 'user.json'
    data = {
        "user_name": encrypt_caesar(user_name, shift_amount),
        "password": encrypt_caesar(password, shift_amount),
    }
    if mode:
        buf = True
        user_data = read_user_file()
        for user in user_data:
            if user["user_name"] == data["user_name"]:
                buf = False
                break
        if buf:
            with open(file_path, 'a') as file:
                json.dump(data, file)
                file.write('\n')
                lab_erorr.configure(text="Регистрация прошла успешно.\nАвторизуйтесь по кнопке ниже и начинайте играть")
        else:
            lab_erorr.configure(text="Имя уже используется!")
    else:
        buf = True
        user_data = read_user_file()
        for user in user_data:
            if user["user_name"] == data["user_name"] and user["password"] == data["password"]:
                buf = False
                break
        if buf:
            lab_erorr.configure(
                text="Неверное имя пользователя или пароль, "
                     "\nповторите попытку или зарегистрируйтесь, \nнажав на кнопку ниже.")
        else:
            main.destroy()
            board()


def read_user_file():
    file_path = 'user.json'
    users = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as json_file:
            for line in json_file:
                data = json.loads(line.strip())
                users.append(data)
    return users


def encrypt_caesar(plaintext, shift):
    ciphertext = ""
    for char in plaintext:
        shifted_char = chr(ord(char) + shift)
        ciphertext += shifted_char
    return ciphertext


def board():
    global game_window
    game_window = Tk()
    game_window.title("Двухходовые шашки – Поддавки")
    game_window.geometry('400x500+100+100')
    game_window.resizable(width=True, height=False)
    game_window.minsize(400, 500)
    global board_canvas
    board_canvas = Canvas(game_window, bg="white", width=400, height=400)
    board_canvas.bind("<Button-1>", click)
    board_canvas.pack(side=TOP)
    board_rendering()
    global lbl_count
    lbl_count = Label(game_window, text=f'Осталось ходов {2 - move_count}')
    lbl_count.pack(side=BOTTOM, pady=(0, 20))
    global  lbl_info
    lbl_info = Label(game_window, text='Ожидание действий')
    lbl_info.pack(side=BOTTOM)
    global lbl_player
    lbl_player = Label(game_window, text='Ход белых')
    lbl_player.pack(side=BOTTOM)
    mainloop()


def click(event):
    x = event.x // 50
    y = event.y // 50
    board_rendering()
    if player_move == 3:
        turn_player_click(x, y)
    else:
        minimax(x, y)


def register():
    main = Tk()
    main.geometry('400x400+100+100')
    main.resizable(width=False, height=False)
    main.title('регистрация')
    lab = Label(text='регистрация')
    lab_name = Label(text='Имя пользователя')
    ent_login = Entry()
    lab_password = Label(text='Пароль')
    ent_password = Entry(show='*')
    lab_repeat_password = Label(text='Повторите пароль')
    ent_repeat_password = Entry(show='*')
    lab_erorr = Label(text="")
    btn_input = Button(text='Ввод', command=lambda window=main,login=ent_login, password=ent_password, repeat_password=ent_repeat_password, error=lab_erorr: input_click_register(main, login, password, repeat_password, error))
    btn_register = Button(text='авторизация', command=lambda window1=main: register_click_register(window1))
    lab.pack(pady=15)
    lab_name.pack()
    ent_login.pack(pady=(0, 15))
    lab_password.pack()
    ent_password.pack(pady=(0, 15))
    lab_repeat_password.pack()
    ent_repeat_password.pack()
    btn_input.pack(pady=10)
    lab_erorr.pack()
    btn_register.pack(side=BOTTOM, pady=20)
    main.mainloop()


def input_click_register(main, ent_login, ent_password, ent_repeat_password, lab_erorr):
    name = ent_login.get()
    password = ent_password.get()
    repeat_password = ent_repeat_password.get()
    if name == '':
        lab_erorr.configure(text="заполните поле 'Имя пользователя'.")
    elif password == '':
        lab_erorr.configure(text="заполните поле 'Пароль'.")
    elif repeat_password == '':
        lab_erorr.configure(text="заполните поле 'Повторите пароль'.")
    else:
        if password != repeat_password:
            lab_erorr.configure(text="Пароли не совпадают!")
        else:
            user_file(name, password, shift_amount, True, lab_erorr, main)


def register_click_register(main):
    main.destroy()
    login_fun()


def login_fun():
    main = Tk()
    main.geometry('400x400+100+100')
    main.resizable(width=False, height=False)
    main.title('авторизация')
    lab = Label(text='авторизация')
    lab_name = Label(text='Имя пользователя')
    ent_login = Entry()
    lab_password = Label(text='Пароль')
    ent_password = Entry(show='*')
    lab_erorr = Label(text="")
    btn_input = Button(text='Ввод', command=lambda window1=main, login=ent_login, password=ent_password, error=lab_erorr: input_click_login(window1, login, password, error))
    btn_register = Button(text='регистрация', command=lambda window1=main: register_click_login(window1))
    lab.pack(pady=15)
    lab_name.pack()
    ent_login.pack(pady=(0, 15))
    lab_password.pack()
    ent_password.pack(pady=(0, 15))
    btn_input.pack(pady=10)
    lab_erorr.pack()
    btn_register.pack(side=BOTTOM, pady=20)
    main.mainloop()


def input_click_login(main, ent_login, ent_password, lab_erorr):
    name = ent_login.get()
    password = ent_password.get()

    if name == '':
        lab_erorr.configure(text="заполните поле 'Имя пользователя'.")
    elif password == '':
        lab_erorr.configure(text="заполните поле 'Пароль'.")
    else:
        user_file(name, password, shift_amount, False, lab_erorr,  main)


def register_click_login(main):
    main.destroy()
    register()


def board_rendering():
    board_canvas.delete("all")
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 1:
                board_canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill="black", outline="black")
                if board_checkers[i][j] == 2:
                    board_canvas.create_oval(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill="red", outline="black")
                if board_checkers[i][j] == 3:
                    board_canvas.create_oval(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill="white", outline="black")
                if board_checkers[i][j] == 12:
                    board_canvas.create_oval(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill="#A20000", outline="black")
                if board_checkers[i][j] == 13:
                    board_canvas.create_oval(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill="#959595", outline="black")


def turn_player_click(x, y):
    global board_checkers
    global player_move
    global move_count
    global click_buf
    global click1
    global click2
    if move_count < 2:
        if board_checkers[y][x] != 2:
            if board_checkers[y][x] == 3 or board_checkers[y][x] == 13:
                if click_stop:
                    click1[0] = y
                    click1[1] = x
                    click_buf = 1
                    lbl_info.configure(text="Шашка выбрана")
            elif board_checkers[y][x] == 0:
                if canvases[y][x] == 1:
                    click2[0] = y
                    click2[1] = x
                    click_buf = 0
                    if board_checkers[click1[0]][click1[1]] == 13:
                        moves, kills, move = queen_check()
                        queen_move(kills, moves, move)
                    else:
                        kill1, kill2, kill3 = check_kill(3)
                        killed_checker(kill1, kill2, kill3)
                else:
                    lbl_info.configure(text="Выберите другой ход")
        else:
            lbl_info.configure(text="Это шашка соперника")
        if move_count == 2:
            move_count = 0
            player_move = 2
            lbl_player.configure(text="Ход красных")
            lbl_count.configure(text=f"Осталось ходов {2 - move_count}")
            check_win()
            minimax(x, y)
    check_win()


def killed_checker(kill1, kill2, kill3):
    global move_count
    global board_checkers
    if len(kill1) > 0:
        if abs(click2[0] - click1[0]) == 2 and abs(click2[1] - click1[1]) == 2:
            moved(kill1, kill2, kill3)
        else:
            lbl_info.configure(text="Нужно съесть вражескую шашку")
    elif len(kill1) == 0:
        if abs(click2[0] - click1[0]) == 1 and abs(click2[1] - click1[1]) == 1:
            one_move()
    else:
        print("сходите в другое место")


def queen_check():
    kill = []
    move = []
    kills = []
    moves = []
    buf_move = []
    k = -1
    p = player_move + 10
    if p == 12:
        p_queen1, p1, p_queen2, p2 = 12, 2, 13, 3
    else:
        p_queen1, p1, p_queen2, p2 = 13, 3, 12, 2
    for y in range(8):
        for x in range(8):
            buf_x = x
            buf_y = y
            if board_checkers[buf_y][buf_x] == p_queen1:
                buf_move.append([buf_y, buf_x])
                kills.append([])
                moves.append([])
                k += 1
                while buf_y > 0 and buf_x > 0:
                    if board_checkers[buf_y - 1][buf_x - 1] == p1 or board_checkers[buf_y - 1][buf_x - 1] == p_queen1:
                        break
                    elif buf_y > 1 and buf_x > 1:
                        if board_checkers[buf_y - 1][buf_x - 1] == p2 or board_checkers[buf_y - 1][buf_x - 1] == p_queen2:
                            if board_checkers[buf_y - 2][buf_x - 2] == 0:
                                move = []
                                kill.append([buf_y - 1, buf_x - 1])
                                move.append([buf_y - 2, buf_x - 2])
                                buf_y -= 1
                                buf_x -= 1
                                while buf_y > 0 and buf_x > 0:
                                    if board_checkers[buf_y - 1][buf_x - 1] == 0:
                                        move.append([buf_y - 1, buf_x - 1])
                                    else:
                                        break
                                    buf_y -= 1
                                    buf_x -= 1
                                if board_checkers[buf_y - 1][buf_x - 1] == 0:
                                    move.append([buf_y - 1, buf_x - 1])
                            else:
                                break
                        elif board_checkers[buf_y - 1][buf_x - 1] == 0:
                            move.append([buf_y - 1, buf_x - 1])
                    else:
                        if board_checkers[buf_y - 1][buf_x - 1] == 0:
                            move.append([buf_y - 1, buf_x - 1])
                    buf_y -= 1
                    buf_x -= 1
                kills[k].append(kill)
                moves[k].append(move)
                kill = []
                move = []
                buf_x = x
                buf_y = y
                while buf_y > 0 and buf_x < 7:
                    if board_checkers[buf_y - 1][buf_x + 1] == p1 or board_checkers[buf_y - 1][buf_x + 1] == p_queen1:
                        break
                    elif buf_y > 1 and buf_x < 6:
                        if board_checkers[buf_y - 1][buf_x + 1] == p2 or board_checkers[buf_y - 1][buf_x + 1] == p_queen2:
                            if board_checkers[buf_y - 2][buf_x + 2] == 0:
                                move = []
                                kill.append([buf_y - 1, buf_x + 1])
                                move.append([buf_y - 2, buf_x + 2])
                                buf_y -= 1
                                buf_x += 1
                                while buf_y > 0 and buf_x < 7:
                                    if board_checkers[buf_y - 1][buf_x + 1] == 0:
                                        move.append([buf_y - 1, buf_x + 1])
                                    else:
                                        break
                                    buf_y -= 1
                                    buf_x += 1
                            else:
                                break
                        elif board_checkers[buf_y - 1][buf_x + 1] == 0:
                            move.append([buf_y - 1, buf_x + 1])
                    else:
                        if board_checkers[buf_y - 1][buf_x + 1] == 0:
                            move.append([buf_y - 1, buf_x + 1])
                    buf_y -= 1
                    buf_x += 1
                kills[k].append(kill)
                moves[k].append(move)
                kill = []
                move = []
                buf_x = x
                buf_y = y
                while buf_y < 7 and buf_x < 7:
                    if board_checkers[buf_y + 1][buf_x + 1] == p1 or board_checkers[buf_y + 1][buf_x + 1] == p_queen1:
                        break
                    elif buf_y < 6 and buf_x < 6:
                        if board_checkers[buf_y + 1][buf_x + 1] == p2 or board_checkers[buf_y + 1][buf_x + 1] == p_queen2:
                            if board_checkers[buf_y + 2][buf_x + 2] == 0:
                                move = []
                                kill.append([buf_y + 1, buf_x + 1])
                                move.append([buf_y + 2, buf_x + 2])
                                buf_y += 1
                                buf_x += 1
                                while buf_y < 6 and buf_x < 6:
                                    if board_checkers[buf_y + 1][buf_x + 1] == 0:
                                        move.append([buf_y + 1, buf_x + 1])
                                    else:
                                        break
                                    buf_y += 1
                                    buf_x += 1
                                if board_checkers[buf_y + 1][buf_x + 1] == 0:
                                    move.append([buf_y + 1, buf_x + 1])
                            else:
                                break
                        elif board_checkers[buf_y + 1][buf_x + 1] == 0:
                            move.append([buf_y + 1, buf_x + 1])
                    else:
                        if board_checkers[buf_y + 1][buf_x + 1] == 0:
                            move.append([buf_y + 1, buf_x + 1])
                    buf_y += 1
                    buf_x += 1
                kills[k].append(kill)
                moves[k].append(move)
                kill = []
                move = []
                buf_x = x
                buf_y = y
                while buf_y < 7 and buf_x > 0:
                    if board_checkers[buf_y + 1][buf_x - 1] == p1 or board_checkers[buf_y + 1][buf_x - 1] == p_queen1:
                        break
                    elif buf_y < 6 and buf_x > 1:
                        if board_checkers[buf_y + 1][buf_x - 1] == p2 or board_checkers[buf_y + 1][buf_x - 1] == p_queen2:
                            if board_checkers[buf_y + 2][buf_x - 2] == 0:
                                move = []
                                kill.append([buf_y + 1, buf_x - 1])
                                move.append([buf_y + 2, buf_x - 2])
                                buf_y += 1
                                buf_x -= 1
                                while buf_y < 6 and buf_x > 1:
                                    if board_checkers[buf_y + 1][buf_x - 1] == 0:
                                        move.append([buf_y + 1, buf_x - 1])
                                    else:
                                        break
                                    buf_y += 1
                                    buf_x -= 1
                                if board_checkers[buf_y + 1][buf_x - 1] == 0:
                                    move.append([buf_y + 1, buf_x - 1])
                            else:
                                break
                        elif board_checkers[buf_y + 1][buf_x - 1] == 0:
                            move.append([buf_y + 1, buf_x - 1])
                    else:
                        if board_checkers[buf_y + 1][buf_x - 1] == 0:
                            move.append([buf_y + 1, buf_x - 1])
                    buf_y += 1
                    buf_x -= 1
                kills[k].append(kill)
                moves[k].append(move)
    board_rendering()
    return moves, kills, buf_move


def queen_move(kills, moves, move):
    global board_checkers
    global click1
    global click2
    global click_stop
    global move_count
    ind = []
    p_queen = player_move + 10
    for i in range(len(kills)):
        for j in range(len(kills[i])):
            if len(kills[i][j]) > 0:
                ind.append([i, j])
    if len(ind) > 0:
        if click1 in move:
            ind_move = move.index(click1)
            kills_move = kills[ind_move]
            moves_move = moves[ind_move]
            for i in range(4):
                if len(kills_move[i]) > 0:
                    if click2 in moves_move[i]:
                        ind = moves_move[i].index(click2)
                        board_checkers[click1[0]][click1[1]] = 0
                        board_checkers[kills_move[i][0][0]][kills_move[i][0][1]] = 0
                        board_checkers[moves_move[i][ind][0]][moves_move[i][ind][1]] = p_queen
                        board_rendering()
                        moves, kills, move = queen_check()
                        ind = []
                        for i1 in range(len(kills)):
                            for j in range(len(kills[i1])):
                                if len(kills[i1][j]) > 0:
                                    ind.append([i1, j])
                        board_rendering()
                        if len(ind) > 0:
                            click_stop = False
                            click1 = click2
                            click2 = [0, 0]
                            board_rendering()
                        else:
                            click_stop = True
                            move_count += 1
                            lbl_count.configure(text=f"Осталось ходов {2 - move_count}")
                            lbl_info.configure(text="Ход выполнен")
                            click1 = [0, 0]
                            click2 = [0, 0]
                            board_rendering()
        else:
            lbl_info.configure(text="Нужно съесть вражескую шашку")
    else:
        flag = False
        kill1, kill2, kill3 = check_kill(player_move)
        if len(kill1) == 0:
            for i in range(len(moves)):
                for j in range(4):
                    if click2 in moves[i][j]:
                        board_checkers[click1[0]][click1[1]] = 0
                        board_checkers[click2[0]][click2[1]] = p_queen
                        board_rendering()
                        move_count += 1
                        lbl_info.configure(text="Ход выполнен")
                        click1 = [0, 0]
                        click2 = [0, 0]
                        flag = True
                        break
                if flag:
                    break
        else:
            lbl_info.configure(text="Нужно съесть вражескую шашку")
    board_rendering()


def moved(kill1, kill2, kill3):
    global board_checkers
    global move_count
    global click_stop
    global click1
    global click2
    ind = -1
    if click1 in kill1:
        c = kill2.count(click2)
        for i in range(c+1):
            ind = kill1.index(click1, ind + 1)
            if ind == kill2.index(click2) or kill2[ind] == click2:
                board_checkers[click1[0]][click1[1]] = 0
                board_checkers[click2[0]][click2[1]] = player_move
                checker_x = kill3[ind][1]
                checker_y = kill3[ind][0]
                board_checkers[checker_y][checker_x] = 0
                board_rendering()
                kill1, kill2, kill3 = check_kill(player_move)
                if click2 in kill1:
                    click_stop = False
                    click1 = click2
                    click2 = [0, 0]
                    break
                else:
                    click_stop = True
                    move_count += 1
                    lbl_count.configure(text=f"Осталось ходов {2 - move_count}")
                    lbl_info.configure(text="Ход выполнен")
                    click1 = [0, 0]
                    click2 = [0, 0]
                    break
            else:
                lbl_info.configure(text="Нужно съесть вражескую шашку")
    board_rendering()
    become_queen()


def one_move():
    global click1
    global click2
    global board_checkers
    global move_count
    moves, kills, move = queen_check()
    ind = []
    for i in range(len(kills)):
        for j in range(len(kills[i])):
            if len(kills[i][j]) > 0:
                ind.append([i, j])
    if len(ind) == 0:
        if click2[0] - click1[0] == 1 and player_move == 2:
            board_checkers[click1[0]][click1[1]] = 0
            board_checkers[click2[0]][click2[1]] = player_move
            move_count += 1
            lbl_count.configure(text=f"Осталось ходов {2 - move_count}")
            lbl_info.configure(text="Ход выполнен")
            click1 = [0, 0]
            click2 = [0, 0]
        elif click2[0] - click1[0] == -1 and player_move == 3:
            board_checkers[click1[0]][click1[1]] = 0
            board_checkers[click2[0]][click2[1]] = player_move
            move_count += 1
            lbl_count.configure(text=f"Осталось ходов {2 - move_count}")
            lbl_info.configure(text="Ход выполнен")
            click1 = [0, 0]
            click2 = [0, 0]
    else:
        lbl_info.configure(text="Нужно съесть вражескую шашку")
    become_queen()
    board_rendering()


def become_queen():
    global board_checkers
    for j in range(1, 8, 2):
        if board_checkers[0][j] == 3:
            board_checkers[0][j] = 13
    for j in range(0, 7, 2):
        if board_checkers[7][j] == 2:
            board_checkers[7][j] = 12
    board_rendering()


def check_kill(p):
    kill1 = []
    kill2 = []
    kill3 = []
    if p == 3:
        for y in range(8):
            for x in range(8):
                if board_checkers[y][x] == 3:
                    if y > 1:
                        if x >= 6 or x <= 1:
                            if x >= 6:
                                if board_checkers[y - 1][x - 1] == 2 or board_checkers[y - 1][x - 1] == 12:
                                    if board_checkers[y - 2][x - 2] == 0:
                                        kill1.append([y, x])
                                        kill2.append([y - 2, x - 2])
                                        kill3.append([y - 1, x - 1])
                            else:
                                if board_checkers[y - 1][x + 1] == 2 or board_checkers[y - 1][x + 1] == 12:
                                    if board_checkers[y - 2][x + 2] == 0:
                                        kill1.append([y, x])
                                        kill2.append([y - 2, x + 2])
                                        kill3.append([y - 1, x + 1])
                        else:
                            if board_checkers[y - 1][x - 1] == 2 or board_checkers[y - 1][x - 1] == 12:
                                if board_checkers[y - 2][x - 2] == 0:
                                    kill1.append([y, x])
                                    kill2.append([y - 2, x - 2])
                                    kill3.append([y - 1, x - 1])
                            if board_checkers[y - 1][x + 1] == 2 or board_checkers[y - 1][x + 1] == 12:
                                if board_checkers[y - 2][x + 2] == 0:
                                    kill1.append([y, x])
                                    kill2.append([y - 2, x + 2])
                                    kill3.append([y - 1, x + 1])
                    if y < 6:
                        if x >= 6 or x <= 1:
                            if x >= 6:
                                if board_checkers[y + 1][x - 1] == 2 or board_checkers[y + 1][x - 1] == 12:
                                    if board_checkers[y + 2][x - 2] == 0:
                                        kill1.append([y, x])
                                        kill2.append([y + 2, x - 2])
                                        kill3.append([y + 1, x - 1])
                            else:
                                if board_checkers[y + 1][x + 1] == 2 or board_checkers[y + 1][x + 1] == 12:
                                    if board_checkers[y + 2][x + 2] == 0:
                                        kill1.append([y, x])
                                        kill2.append([y + 2, x + 2])
                                        kill3.append([y + 1, x + 1])
                        else:
                            if board_checkers[y + 1][x - 1] == 2 or board_checkers[y + 1][x - 1] == 12:
                                if board_checkers[y + 2][x - 2] == 0:
                                    kill1.append([y, x])
                                    kill2.append([y + 2, x - 2])
                                    kill3.append([y + 1, x - 1])
                            if board_checkers[y + 1][x + 1] == 2 or board_checkers[y + 1][x + 1] == 12:
                                if board_checkers[y + 2][x + 2] == 0:
                                    kill1.append([y, x])
                                    kill2.append([y + 2, x + 2])
                                    kill3.append([y + 1, x + 1])
    else:
        for y in range(8):
            for x in range(8):
                if board_checkers[y][x] == 2:
                    if y < 6:
                        if x >= 6 or x <= 1:
                            if x > 5:
                                if board_checkers[y + 1][x - 1] == 3 or board_checkers[y + 1][x - 1] == 13:
                                    if board_checkers[y + 2][x - 2] == 0:
                                        kill1.append([y, x])
                                        kill2.append([y + 2, x - 2])
                                        kill3.append([y + 1, x - 1])
                            else:
                                if board_checkers[y + 1][x + 1] == 3 or board_checkers[y + 1][x + 1] == 13:
                                    if board_checkers[y + 2][x + 2] == 0:
                                        kill1.append([y, x])
                                        kill2.append([y + 2, x + 2])
                                        kill3.append([y + 1, x + 1])
                        else:
                            if board_checkers[y + 1][x - 1] == 3 or board_checkers[y + 1][x - 1] == 13:
                                if board_checkers[y + 2][x - 2] == 0:
                                    kill1.append([y, x])
                                    kill2.append([y + 2, x - 2])
                                    kill3.append([y + 1, x - 1])
                            if board_checkers[y + 1][x + 1] == 3 or board_checkers[y + 1][x + 1] == 13:
                                if board_checkers[y + 2][x + 2] == 0:
                                    kill1.append([y, x])
                                    kill2.append([y + 2, x + 2])
                                    kill3.append([y + 1, x + 1])
                    if y > 1:
                        if x >= 6 or x <= 1:
                            if x > 5:
                                if board_checkers[y - 1][x - 1] == 3 or board_checkers[y - 1][x - 1] == 13:
                                    if board_checkers[y - 2][x - 2] == 0:
                                        kill1.append([y, x])
                                        kill2.append([y - 2, x - 2])
                                        kill3.append([y - 1, x - 1])
                            else:
                                if board_checkers[y - 1][x + 1] == 3 or board_checkers[y - 1][x - 1] == 13:
                                    if board_checkers[y - 2][x + 2] == 0:
                                        kill1.append([y, x])
                                        kill2.append([y - 2, x + 2])
                                        kill3.append([y - 1, x + 1])
                        else:
                            if board_checkers[y - 1][x - 1] == 3 or board_checkers[y - 1][x - 1] == 13:
                                if board_checkers[y - 2][x - 2] == 0:
                                    kill1.append([y, x])
                                    kill2.append([y - 2, x - 2])
                                    kill3.append([y - 1, x - 1])
                            if board_checkers[y - 1][x + 1] == 3 or board_checkers[y - 1][x - 1] == 13:
                                if board_checkers[y - 2][x + 2] == 0:
                                    kill1.append([y, x])
                                    kill2.append([y - 2, x + 2])
                                    kill3.append([y - 1, x + 1])
    return kill1, kill2, kill3


def minimax_one_move():
    global click1
    global click2
    move_click1 = []
    move_click2 = []
    count = 0
    for i in range(8):
        for j in range(8):
            if board_checkers[i][j] == player_move:
                move_click2.append([])
                move_click1.append([i, j])
                if i + 1 < 8:
                    for j1 in range(8):
                        if abs(j - j1) == 1:
                            if board_checkers[i + 1][j1] == 0 and canvases[i + 1][j1] == 1:
                                #click2 = [i + 1, j1]
                                move_click2[count].append([i + 1, j1])
                    count += 1
    ind = []
    for i in range(len(move_click2)):
        if move_click2[i] == []:
            ind.append(i)
    ind.reverse()
    for i in ind:
        move_click1.pop(i)
        move_click2.pop(i)
    if move_click1 != 0:
        ind = randint(0, len(move_click1)-1)
        click1 = move_click1[ind]
        click2 = move_click2[ind][randint(0, len(move_click2[ind])-1)]
        one_move()
    board_rendering()
    return


def minimax(x, y):
    global player_move
    global move_count
    global click_buf
    global click1
    global click2
    if move_count < 2:
        moves, kills, move = queen_check()
        kill1, kill2, kill3 = check_kill(player_move)

        ind = []
        for j in range(len(kills)):
            for i in range(len(kills[j])):
                if kills[j][i] != []:
                    ind.append(i)

        if len(ind) > 0:
            i = randint(0, len(kills)-1)
            click1 = move[i]
            ind = []
            for j in range(4):
                if moves[i][j] == []:
                    ind.append(j)
            ind.reverse()
            for j in ind:
                moves[i].pop(j)
            buf1 = moves[i][randint(0, len(moves[i])-1)]
            buf2 = buf1[randint(0, len(buf1) - 1)]
            click2 = buf2
            moves, kills, move = queen_check()
            queen_move(kills, moves, move)
        elif len(kill1) > 0 and move_count < 2:
            i = randint(0, len(kill1)-1)
            click1 = kill1[i]
            click2 = kill2[i]
            killed_checker(kill1, kill2, kill3)
        elif move_count < 2:
            if randint(0, 1) == 0:
                if len(moves) != 0:
                    i = randint(0, len(move) - 1)
                    click1 = move[i]
                    ind = []
                    for j in range(4):
                        if moves[i][j] == []:
                            ind.append(j)
                    ind.reverse()
                    for j in ind:
                        moves[i].pop(j)

                    buf1 = moves[i][randint(0, len(moves[i]) - 1)]
                    buf2 = buf1[randint(0, len(buf1) - 1)]
                    click2 = buf2
                    queen_move(kills, moves, move)
            else:
                minimax_one_move()
        if move_count == 2:
            move_count = 0
            player_move = 3
            lbl_player.configure(text="Ход белых")
            lbl_count.configure(text=f"Осталось ходов {2 - move_count}")
            return
    board_rendering()
    check_win()


def check_win():
    c1 = 0
    c2 = 0
    for i in range(8):
        c1 += board_checkers[i].count(2) + board_checkers[i].count(12)
        c2 += board_checkers[i].count(3) + board_checkers[i].count(13)
    if c1 == 0:
        lbl_text = "Победили красные"
    elif c2 == 0:
        lbl_text = "Победили белые"
    if c1 == 0 or c2 == 0:
        info = Toplevel()
        info.title("Конец игры")
        info.geometry("200x200+100+100")
        info.resizable(width=False, height=False)
        info.grab_set()
        lbl = Label(info, text=lbl_text, width=18, font="20")
        btn_ok = Button(info, text="Ок", width=5, command=lambda window2=info: close_game(window2))
        btn_continue = Button(info, text="Ёще раз", width=10, command=lambda window2=info: game_restart(window2))
        lbl.grid(column=0, row=0, pady=20)
        btn_ok.grid(column=0, row=2, pady=15)
        btn_continue.grid(column=0, row=3)


def close_game(info):
    global game_window
    info.destroy()
    game_window.destroy()


def game_restart(info):
    global game_window
    global board_checkers_start
    global board_checkers
    global move_count
    global player_move
    info.destroy()
    game_window.destroy()
    move_count = 0
    player_move = 3
    board_checkers = copy.deepcopy(board_checkers_start)
    board()

login_fun()

