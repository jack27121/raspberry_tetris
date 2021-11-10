import time
from sense_hat import SenseHat
import numpy as np

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

#Tetronimo pieces
piece_i = np.array([
    [blank,light_blue,blank],
    [blank,light_blue,blank],
    [blank,light_blue,blank],
    [blank,light_blue,blank]
])
piece_s = np.array([
    [blank,green,green],
    [green,green,blank]
])
piece_l = np.array([
    [blank,orange,blank],
    [blank,orange,blank],
    [blank,orange,orange]
])
piece_t = np.array([
    [blank,blank,blank],
    [purple,purple,purple],
    [blank,purple,blank]
])
piece_j = np.array([
    [blank,blue,blank],
    [blank,blue,blank],
    [blue,blue,blank]
])
piece_o = np.array([
    [yellow,yellow],
    [yellow,yellow]
])
piece_z = np.array([
    [red,red,blank],
    [blank,red,red]
])

#The stationary field
field_static = np.ones((8,8,3),int)
field_static[:,:] = blank

#the active field
field = field_static.copy()

piece = piece_t

x = 3
y = 0
input_x = 0
input_y = 0
rotate = False

t = 0

def step():
    global field

    delta_field = collision_movement(input_x,input_y,rotate)
    if(type(delta_field) != bool): field = delta_field

    hat.clear()
    hat.set_pixels(field.reshape(64,3))
    

def stick(event):
    #gets input variables
    global input_x, input_y, rotate
    if event.action in ('pressed', 'held'):
        #region input
        input_x= {
            'left': -1,
            'right': 1,
        }.get(event.direction, 0)
        input_y= {
            'up': -1,
            'down': 1,
        }.get(event.direction, 0)
        rotate= {
            'middle': True
        }.get(event.direction, False)

def collision_movement(input_x,input_y,rotate):
    # returns the new updated field, or false if there was collissions
    global x, y

    input_x += x
    input_y += y

    delta_field = field.copy()

    if(rotate):
        new_piece = np.rot90(piece,-1)
    else: new_piece = piece
    
    for x_ in range(0, new_piece.shape[1]):
        for y_ in range(0, new_piece.shape[0]):
            #it doesn't check blank parts of piece
            if(np.array_equal(new_piece[x_,y_],blank)): continue
            #writes to new_field
            if (np.array_equal(delta_field[x_+input_x,y_+input_y],blank)): 
                    delta_field[x_+input_x,y_+input_y] = new_piece[x_,y_]
            else: return False
    print(delta_field)
    return delta_field
    

def clamp(value, min_value=0, max_value=7):
    return min(max_value, max(min_value, value))

def pieceRotate():
    global piece
    piece = np.rot90(piece,-1)

while True:
    t += time.process_time()
    input_x = 0
    input_y = 0
    rotate = False
    for event in hat.stick.get_events():
        stick(event)
    step()
    time.sleep(0.1)
