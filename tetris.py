from os import wait
import time
import random
from sense_hat import SenseHat
import numpy as np
import signal
import sys

hat = SenseHat()

#colors
blank       = np.array([0,0,0])
light_blue  = np.array([0,255,255])
yellow      = np.array([255,255,0])
purple      = np.array([128,0,128])
green       = np.array([0,255,0])
red         = np.array([255,0,0])
blue        = np.array([0,0,255])
orange      = np.array([255,127,0])

#blank row
blank_row = np.array([blank,blank,blank,blank,blank,blank,blank,blank])

#Tetronimo pieces
piece_i = np.array([
    [light_blue,light_blue,light_blue,light_blue],
    [blank,blank,blank,blank],
    [blank,blank,blank,blank],
    [blank,blank,blank,blank]
])
piece_s = np.array([
    [blank,green,green],
    [green,green,blank]
])
piece_z = np.array([
    [red,red,blank],
    [blank,red,red]
])
piece_l = np.array([
    [blank,orange,blank],
    [blank,orange,blank],
    [blank,orange,orange]
])
piece_j = np.array([
    [blank,blue,blank],
    [blank,blue,blank],
    [blue,blue,blank]
])
piece_t = np.array([
    [blank,blank,blank],
    [purple,purple,purple],
    [blank,purple,blank]
])
piece_o = np.array([
    [yellow,yellow],
    [yellow,yellow]
])


#The stationary field
static_field = np.ones((8,8,3),int)
static_field[:,:] = blank

#the active field
field = static_field.copy()

rotation = 0
input_x = 0
input_y = 0
input_rotate = 0

def restart():
    #resets program
    global static_field, field
    #The stationary field
    static_field[:,:] = blank

    #the active field
    field = static_field.copy()
    random_piece()


def step():
    #every step this gets ran
    global field, static_field, input_x,input_y,input_rotate

    delta_field = collision_movement(input_x,input_y,input_rotate)
    input_x = 0
    input_y = 0
    input_rotate = 0

    if(type(delta_field) == bool):
        if(delta_field == True):
            static_field = field
            clear_rows()
            random_piece()
    else: 
        field = delta_field
    
    hat.clear()
    hat.set_pixels(field.reshape(64,3))
    
def clear_rows():
    #loops through all the rows, and clears them if they're filled
    global static_field

    for row in reversed(range(0,static_field.shape[0])):
        while(np.all(np.any(static_field[row,:],axis=1))):
            static_field = np.delete(static_field,row,0)
            static_field = np.insert(static_field, 0, blank_row, axis=0)


def stick(event):
    #gets input variables
    global input_x, input_y, input_rotate
    if event.action in ('pressed', 'held'):
        input_y= {
            'left': -1,
            'right': 1,
        }.get(event.direction, 0)

        if(event.direction == 'down'):
            input_x = 1
        else:
            input_x = 0

        input_rotate= {
            'up': 1
        }.get(event.direction, 0)

def collision_movement(input_x,input_y,input_rotate):
    # returns the new updated field, true if bottom is reached, else false
    global x, y, rotation

    delta_field = static_field.copy()
    new_piece = np.rot90(piece,rotation-input_rotate)
    
    for x_ in range(0, new_piece.shape[0]):
        for y_ in range(0, new_piece.shape[1]):
            #it doesn't check blank parts of piece
            if(np.array_equal(new_piece[x_,y_],blank)): continue
            #writes to new_field
            block_x = x_+x+input_x
            block_y = y_+y+input_y

            collission = False
            try:
                if (np.array_equal(static_field[block_x,block_y],blank) and within(block_x) and within(block_y)): 
                    delta_field[block_x,block_y] = new_piece[x_,y_]
                else: collission = True
            except: collission = True
            if(collission):
                if(input_y == 0 and input_x == 1): return True
                else: return False
    x+=input_x
    y+=input_y
    rotation-=input_rotate
    return delta_field
    

def within(value, min_value=0, max_value=7):
    #returns if value is within min and max value
    return ((value >= min_value) and (value <= max_value))

ran = random
def random_piece():
    #selects a new random piece and sets it's initial x,y values
    global piece, x, y
    x = -1
    y = 3
    n = ran.randint(0,6)
    if n == 0:
        piece = piece_i
        x = -2
        y = 2
    elif n == 1:
        piece = piece_s
    elif n == 2:
        piece = piece_z
    elif n == 3:
        piece = piece_l
        y = 2
    elif n == 4:
        piece = piece_j
    elif n == 5:
        piece = piece_t
        x = -2
    elif n == 6:
        piece = piece_o

def signal_term_handler(signal, frame):
    hat.show_message("TETRIS")
    sys.exit(0)
 
signal.signal(signal.SIGTERM, signal_term_handler)

signal.signal(signal.SIGINT, signal_term_handler)

restart()
hat.stick.direction_up = stick
hat.stick.direction_down = stick
hat.stick.direction_left = stick
hat.stick.direction_right = stick
hat.stick.direction_any = step
hat.stick.direction_middle = restart

while True:
    step()
    input_x = 1
    time.sleep(0.4)
