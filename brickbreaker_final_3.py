"""
File: brickbreaker.py
----------------
YOUR DESCRIPTION HERE
"""

import tkinter
import time
import random

# How big is the playing area?              
CANVAS_WIDTH = 600      # Width of drawing canvas in pixels
CANVAS_HEIGHT = 650     # Height of drawing canvas in pixels

# Constants for the bricks
N_ROWS = 8              # How many rows of bricks are there?
N_COLS = 2             # How many columns of bricks are there?
SPACING = 5             # How much space is there between each brick?
BRICK_START_Y = 50      # The y coordinate of the top-most brick
BRICK_HEIGHT = 20       # How many pixels high is each brick
BRICK_WIDTH = (CANVAS_WIDTH - (N_COLS+1) * SPACING ) / N_COLS

# Constants for the ball and paddle
BALL_SIZE = 40
PADDLE_Y = CANVAS_HEIGHT - 40
PADDLE_WIDTH = 80

def main():
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Brick Breaker')
    # TODO: your code here
    create_bricks(canvas)
    
    x_start = (CANVAS_WIDTH - BALL_SIZE)/2
    y_start = (CANVAS_HEIGHT - BALL_SIZE)/2
    x_end = (CANVAS_WIDTH + BALL_SIZE)/2
    y_end = (CANVAS_HEIGHT + BALL_SIZE)/2
    
    ball = canvas.create_oval(x_start, y_start, x_end, y_end, fill ='black')
    

    x_start_paddle = (CANVAS_WIDTH - PADDLE_WIDTH)/2
    y_start_paddle = 600
    x_end_paddle = (CANVAS_WIDTH + BALL_SIZE)/2
    y_end_paddle = 620
    
    paddle = canvas.create_rectangle(x_start_paddle, y_start_paddle, x_end_paddle, y_end_paddle, fill ='black')
    change_x = random.randint(1,4)
    change_y = random.randint(7,9)

    count = 0
    no_of_bricks = N_COLS * N_ROWS
    lives = 3
    
    text_score_title = canvas.create_text(10, 10, anchor='w', font=('Arial',12,'bold'), text='Bricks Remaining: ', fill = 'red')
    text_score = canvas.create_text(160, 10, anchor='w', font=('Arial',12,'bold'), text=str(no_of_bricks), fill = 'red')
    text_lives_title = canvas.create_text(10, 30, anchor='w', font=('Arial',12,'bold'), text='Lives Remaining: ', fill = 'red')
    text_lives = canvas.create_text(160, 30, anchor='w', font=('Arial',12,'bold'), text= str(lives), fill = 'red')
    

    while no_of_bricks != 0 and lives != 0:
            
        canvas.move(ball,change_x,change_y)       

        mouse_x = canvas.winfo_pointerx()
        dx = mouse_x - canvas.coords(paddle)[0]

        if canvas.coords(paddle)[0] +PADDLE_WIDTH + dx >= CANVAS_WIDTH:
            dx = dx/10

        if canvas.coords(paddle)[2] + dx <= CANVAS_WIDTH:
            canvas.move(paddle,dx,0)



        ball_coords = canvas.coords(ball)

        x_1 = ball_coords[0]
        y_1 = ball_coords[1]
        x_2 = ball_coords[2]
        y_2 = ball_coords[3]

        colliding_list = canvas.find_overlapping(x_1, y_1, x_2, y_2)
        

        for obj in colliding_list:
            if obj == paddle:
                change_y *=-1
            elif obj != ball and obj != paddle and obj != text_score and obj != text_lives and obj != text_score_title and obj != text_lives_title:
                canvas.delete(obj)
                count += 1
                no_of_bricks -= 1
                if (change_x >= 0 and change_y <= 0) or (change_x < 0 and change_y < 0):
                    change_y *= -1
                if (change_x > 0 and change_y > 0) or (change_x < 0 and change_y > 0):
                    change_x *= -1
        
        if hit_left_wall(canvas, ball) or hit_right_wall(canvas, ball):
            change_x *= -1
        if hit_top_wall(canvas, ball): 
        #or hit_bottom_wall(canvas,ball)
            change_y *= -1

        if hit_bottom_wall(canvas,ball):
            lives -= 1          
            canvas.delete(ball)
            change_x = random.randint(1,4)
            change_y = random.randint(7,9) 
            ball = canvas.create_oval(x_start, y_start, x_end, y_end, fill ='black')  

        canvas.delete(text_score)
        text_score = canvas.create_text(160, 10, anchor='w', font= ('Arial',12,'bold'), text=str(no_of_bricks), fill = 'red')


        canvas.delete(text_lives)
        text_lives = canvas.create_text(160, 30, anchor='w', font=('Arial',12,'bold'), text=str(lives), fill = 'red',)

        canvas.update()
        time.sleep(1/50)

    if no_of_bricks == 0:
        canvas1 = make_canvas(400, 300, 'You Win')
        canvas1.create_text(200,100,text = 'Congratulations!!! You Win!!!', fill = 'red', font = ('Arial',20,'bold'))
        canvas1.create_text(200,150,text = 'Bricks Remaining: ' + str(no_of_bricks), fill = 'red', font = ('Arial',20,'bold'))
        canvas1.create_text(200,200,text = 'Lives Remaining: ' + str(lives), fill = 'red', font = ('Arial',20,'bold'))

    if lives == 0:
        canvas1 = make_canvas(400, 300, 'Game Over')
        canvas1.create_text(200,100,text = 'Game over!!! ', fill = 'red', font = ('Arial',20,'bold'))
        canvas1.create_text(200,150,text = 'You have ' + str(lives) + ' lives remaining.', fill = 'red', font = ('Arial',20,'bold'))
        canvas1.create_text(200,200,text = 'Bricks Remaining: ' + str(no_of_bricks), fill = 'red', font = ('Arial',20,'bold'))


    canvas.mainloop()


def hit_left_wall(canvas, object):
    return get_left_x(canvas, object) <= 0

def hit_top_wall(canvas, object):
    return get_top_y(canvas, object) <= 0

def hit_right_wall(canvas, object):
    return get_right_x(canvas, object) >= CANVAS_WIDTH

def hit_bottom_wall(canvas, object):
    return get_bottom_y(canvas, object) >= CANVAS_HEIGHT


def get_top_y(canvas, object):
    '''
    This friendly method returns the y coordinate of the top of an object.
    Recall that canvas.coords(object) returns a list of the object 
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 1 is the top-y
    '''
    return canvas.coords(object)[1]

def get_left_x(canvas, object):
    '''
    This friendly method returns the x coordinate of the left of an object.
    Recall that canvas.coords(object) returns a list of the object 
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 0 is the left-x
    '''
    return canvas.coords(object)[0]

def get_right_x(canvas, object):
    '''
    This friendly method returns the x coordinate of the left of an object.
    Recall that canvas.coords(object) returns a list of the object 
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 0 is the left-x
    '''
    return canvas.coords(object)[2]



def get_bottom_y(canvas, object):
    '''
    This friendly method returns the x coordinate of the left of an object.
    Recall that canvas.coords(object) returns a list of the object 
    bounding box: [x_1, y_1, x_2, y_2]. The element at index 0 is the left-x
    '''
    return canvas.coords(object)[3]


def make_canvas(width, height, title):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas

def create_bricks(canvas):

    color = ['red','red','dark orange','dark orange','chartreuse2','chartreuse2','cyan','cyan']

    y_start = []
    for i in range(N_ROWS):
        y_start.append(BRICK_START_Y + i* BRICK_HEIGHT + i * SPACING)

    x_start = []
    for i in range(N_COLS):
        x_start.append(0 + i * (BRICK_WIDTH + SPACING))

    for row in range(N_ROWS):
        for column in range(N_COLS):

            x_end = x_start[column] + BRICK_WIDTH
            y_end =  y_start [row] + BRICK_HEIGHT

            canvas.create_rectangle(x_start[column], y_start[row], x_end , y_end, fill = color[row], outline = color[row])








    
    

        
        
        
       

       









if __name__ == '__main__':
    main()
