from math import sqrt
from tkinter import *
import random
from tkinter import messagebox

# Hàm di chuyển ball, direct là chiều di chuyển bóng, speed là tốc độ, hàm start stop để start stop trò chơi
direct_xy = list (range (-3, 3))
direct_xy.remove (0)
direct_x = random.choice (direct_xy)
direct_y = random.choice (direct_xy) * direct_x
speed = int ( 4000 * sqrt ((direct_y**2 + direct_x**2)) / 500)
play = 1


def exit ():
    response = messagebox.askyesno ("Exit!", "Do you want to exit?")
    if response == 1:
        return playboard.destroy ()
    else:
        return
    
def start_stop ():
    def start ():
        global play
        play = 1
        btn_play.config (text="Pause")
        move_ball ()
    def pause ():
        global play
        btn_play.config (text="Resume")
        play = -1
    if btn_play['text'] == "Start" or btn_play['text'] == "Resume":
        return start ()
    elif btn_play['text'] == "Pause":
        return pause ()

def reset (end = 0):
    global play, direct_x, direct_y, speed, score, ball, bar
    if end == 0: # Mặc định chưa thua, hỏi để reset game.
        response = messagebox.askyesno ("Reset!", "Do you want to reset the game?")
    else: # end = 1, thông báo thua
        response = messagebox.askyesno (title="Game end!", message=f"Your score: {score}\nDo you want to play again?")
        
    if response == 1: # Nếu muốn chơi lại reset game.
        play = -1
        direct_x = random.choice (direct_xy)
        direct_y = random.choice (direct_xy) * direct_x
        speed = int ( 4000 * sqrt ((direct_y**2 + direct_x**2)) / 500)
        score = 0
        score_label.config (text="Score: {}".format(score))
        btn_play.config (text="Start")
        canvas.delete (ball, bar)
        ball = canvas.create_oval (x0-r, y0, x0+r, y0+2*r, fill="blue")
        bar = canvas.create_rectangle (245, 500, 335, 510, fill="brown")
    else:
        return
        
def impact (): # Hàm va chạm, r=10 bán kính ball; chiều rộng bar=90, y1_bar = 500, y2_bar = 510, tìm điểm A thuộc bar gần ball nhất
    global r
    x_ball = (canvas.coords (ball)[0] + canvas.coords (ball)[2]) / 2
    y_ball = (canvas.coords (ball)[1] + canvas.coords (ball)[3]) / 2
    x_bar = (canvas.coords (bar)[0] + canvas.coords (bar)[2]) / 2
    if x_ball < x_bar - 45: # tìm tọa độ x_A của điểm A thuộc bar gần ball nhất
        x_A = x_bar - 45
    elif x_ball > x_bar + 45:
        x_A = x_bar + 45
    else:
        x_A = x_ball
    
    if y_ball < 500: # tìm tọa độ y_A của điểm A thuộc bar gần ball nhất
        y_A = 500
    elif y_ball > 510:
        y_A = 510
    else:
        y_A = y_ball

    if sqrt((x_ball - x_A)**2 + (y_ball - y_A)**2) <= r: # Khoảng cách A đên tâm ball <= r có va chạm
        return True
    else:
        return False

def move_ball ():
    global direct_x, direct_y, speed, play, score
    if play == -1:
        return

    # Chạm biên trái phải, đổi hướng direct_x
    if canvas.coords (ball)[0] + direct_x < 20:
        x = 20 - canvas.coords (ball)[0]
        y = direct_y * (x / direct_x)
        direct_x *= -1
    elif canvas.coords (ball)[2] + direct_x > 560:
        x = 560 - canvas.coords (ball)[2]
        y = direct_y * (x / direct_x)
        direct_x *= -1
    else:
        x = direct_x
        y = direct_y
    
    # Chạm biên trên đổi hướng direct_y, chạm dưới stop, you lose
    if canvas.coords (ball)[1] + direct_y < 20:
        y = 20 - canvas.coords (ball)[1]
        x = direct_x * (y / direct_y)
        direct_y *= -1
    elif canvas.coords (ball)[3] >= 500: # Nếu y ball >= 500 (độ cao bar), xét tiếp chạm biên dưới thì thua, ko thì chạy tiếp
        if canvas.coords (ball)[3] + direct_y > 560:
            y = 560 - canvas.coords (ball)[3]
            x = direct_x * (y / direct_y)
            start_stop ()
            reset (1)
        else: # y_ball chưa vượt quá 560
            if impact () == True: # Nếu có va chạm đổi hướng direct_x (vì y_ball > 500, nếu va chạm xảy ra sẽ nằm bên cạnh bar)
                if (direct_x > 0 and canvas.coords (ball)[0] < canvas.coords (bar)[0]) \
                    or (direct_x < 0 and canvas.coords (ball)[2] > canvas.coords (bar)[2]):
                    direct_x *= -1
                else: # Va chạm thuận chiều di chuyển của ball thì tăng tốc di chuyển
                    direct_x *= 2
            x = direct_x
            y = direct_y   
    elif canvas.coords (ball)[3] + direct_y >= 500: # Nếu y ball (<500) + direct_y > 500 thì move ball đến y = 500, xét va chạm với bar     
        y1 = 500 - canvas.coords (ball)[3]
        x1 = direct_x * (y / direct_y)
        canvas.move (ball, x1, y1)
        if impact () == True: # Nếu có va chạm đổi hướng direct_y (vì y_ball < 500, nếu va chạm xảy ra sẽ nằm trên bar).
            direct_y *= -1
            score += 10
            score_label.config (text="Score: {}".format(score))
            speed = speed*9//10
        x = direct_x
        y = direct_y
    
    canvas.move (ball, x, y)
    canvas.after (speed, move_ball)

# Hàm di chuyển thanh bar đỡ bóng sang phải, gắn với sự kiện phím right được nhấn
def right (event):
    if canvas.coords (bar)[2] + 30 < 560:
        x = 30
    else:
        x = 560 - canvas.coords (bar)[2]
    y = 0
    canvas.move (bar, x, y)

# Hàm di chuyển thanh bar đõ bóng sang trái, gắn với sự kiện phím left được nhấn 
def left (event):
    if canvas.coords (bar)[0] - 30 > 20:
        x = - 30
    else:
        x = 20 - canvas.coords (bar)[0]
    y = 0
    canvas.move (bar, x, y)

# Tạo cửa sổ playboard, trò chơi diễn ra trong cửa sổ này
playboard = Tk ()
playboard.title ("Bouncing Ball Game")
playboard.geometry ("620x700")

# Label score hiển thị điểm
score = 0
score_label = Label (playboard, text="Score: {}".format(score))
score_label.grid (row=0, column=1, pady=10, sticky="s")

# Khung trò chơi
canvas = Canvas (playboard, width= 560, height= 560)
canvas.create_rectangle (20, 20, 560, 560, fill="white")

# r là bán kính ball, x0 điểm x giữa khung play, y0=20 điểm y viền trên khung
r = 12
x0 = 290
y0 = 20

# Tạo bóng với vị trí đầu giữa khung trên cùng
ball = canvas.create_oval (x0-r, y0, x0+r, y0+2*r, fill="blue")

# Tạo thanh bar đỡ bóng với vị trí đầu giữa khung cách đáy 50
bar = canvas.create_rectangle (245, 500, 335, 510, fill="brown")

# Grid canvas
canvas.grid (row=1, column=0, columnspan=3, padx=20, pady=0)

# Các button chức lựa chọn
btn_play = Button (playboard, width=5, text="Start", command=start_stop)
btn_reset = Button (playboard, width=5, text="Reset", command=reset)
btn_exit = Button (playboard, width=5, text="Exit", command=exit)

# Grid button
btn_play.grid (row=2, column=0, pady=30)
btn_reset.grid (row=2, column=1, pady=30)
btn_exit.grid (row=2, column=2, pady=30)

# Bind sự kiện nhấn phím với hàm điều khiển thanh bar
playboard.bind ("<Right>", right)
playboard.bind ("<Left>", left)

# Playboard mainloop
playboard.mainloop ()