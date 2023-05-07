from tkinter import *
import random

running = True
WIDTH = 400
HEIGHT = 642
xmove = 10
ball_move_x =  2
ball_move_y = -random.randint(1, 5)
x1, x2, y1, y2 = 10, 580, 90, 600
bricks = []
score = 0

# create the window and the canvas
window = Tk()
window.title('Arkanoid')
window.iconbitmap("arkanoid.ico")
label = Label(window, bg="black", fg="green", font=("Arial", 24), text="SCORE: ")
label.pack()
canvas = Canvas(window, width=WIDTH, height=HEIGHT,bg='light grey')
canvas.pack()
window.update()

# get the window dimensions
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# find the center point
center_x = int(screen_width / 2 - WIDTH / 2)
center_y = int(screen_height / 2 - HEIGHT / 2) - 50

# set the position of the window to the center of the screen
window.geometry(f"{WIDTH}x{HEIGHT}+{center_x}+{center_y}")
# print("label width: ", label.winfo_height())


main_board = canvas.create_rectangle(x1, x2, y1, y2, fill="black")
ball = canvas.create_oval(
    WIDTH / 2, HEIGHT / 2, (WIDTH / 2) + 25, (HEIGHT / 2) + 25, fill="red"
)


# create the blocks and give random colors
def blocks():
    x = 0
    y = 50
    gap = 30
    colors = ["red", "green", "blue", "yellow"]
    for i in range(7):
        for j in range(4):
            bricks.append(
                canvas.create_rectangle(
                    (x + 60) * i,
                    y + (gap * j),
                    ((x + 60) * i) + 40,
                    y + 20 + (j * gap),
                    fill=colors[(random.randint(0, 3))],
                )
            )
    return


# give ball movement and react on collision
def move_ball():
    global ball_move_x
    global ball_move_y
    global bricks
    global score

    if running:
        try:
            x1, y1, x2, y2 = canvas.coords(ball)
            brick = get_brick()
            if bricks == []:
                game_over()
            if brick:
                ball_move_y = -ball_move_y
                canvas.delete(brick)
                bricks.pop(bricks.index(brick))
                score += 10
                label.config(text="SCORE: " + str(score))
                window.update()
            if (x1 <= 0) or (x2 >= WIDTH):
                ball_move_x = -ball_move_x
            if y1 <= 0:
                ball_move_y = -ball_move_y
            if y2 >= HEIGHT - 60:
                collision()
            canvas.move(ball, ball_move_x, ball_move_y)
            canvas.after(5, move_ball)
        except ValueError:
            pass


# key function
def right_key(event):
    global xmove
    global main_board
    try:
        x1, y1, x2, y2 = canvas.coords(main_board)
        if x2 < WIDTH:
            canvas.delete(main_board)
            main_board = canvas.create_rectangle(
                x1 + xmove, 580, x2 + xmove, 600, fill="black"
            )
    except ValueError:
        pass


def left_key(event):
    global xmove
    global main_board
    try:
        x1, y1, x2, y2 = canvas.coords(main_board)
        if x1 > 0:
            canvas.delete(main_board)
            main_board = canvas.create_rectangle(
                x1 - xmove, 580, x2 - xmove, 600, fill="black"
            )
    except ValueError:
        pass


# check for collision events and react
def collision():
    boardx1, boardy1, boardx2, boardy2 = canvas.coords(main_board)
    ballx1, bally1, ballx2, bally2 = canvas.coords(ball)
    global ball_move_y
    if bally2 > HEIGHT:
        game_over()
    if (ballx1 + ballx2) / 2 > boardx1 and (ballx1 + ballx2) / 2 < boardx2:
        ball_move_y = -ball_move_y


# print game over screen
def game_over():
    global running
    running = False
    canvas.delete(main_board)
    canvas.delete(ball)
    label_over = Label(
        window, bg="black", fg="green", font=("Arial", 24), text="GAME OVER!"
    )
    label_over.place(x=90, y=300)
    window.update()
    return


# if ball hits a block return the specific brick from the list
def get_brick():
    ballx1, bally1, ballx2, bally2 = canvas.coords(ball)
    ball_vx = (ballx1 + ballx2) / 2
    ball_vy = (bally1 + bally2) / 2 

    for brick in bricks:
        x1, y1, x2, y2 = canvas.coords(brick)
        if x1 < ball_vx < x2 and (ball_vy - 12)< y2 and (ball_vy + 12) > y1:
            return brick


blocks()
move_ball()


window.bind("<Left>", left_key)
window.bind("<Right>", right_key)
window.mainloop()
