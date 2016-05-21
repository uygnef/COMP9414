import random
from socket import *

dirn = 3
world = [[' ' for _ in range(80)]for _ in range(80)]
row = 40
colum = 40
stone = False
prior_action = None
have_been = set((colum,row))
can_go = [' ','o']

def go_to(point):
    global dirn
    global prior_action

def hang_out(view):
    global dirn
    global stone
    global prior_action
    global can_go
    # find the area that can go but have not been   
    #stack = [] #save the dirction order by the prioritize

    hang = []
    if view[1][2] in can_go:
        hang.append('f')
        hang.append('f')
        hang.append('f')
        hang.append('f')
        hang.append('f')
        hang.append('f')

    if view[2][3] in can_go:
        hang.append('r')
        hang.append('r')

    if view[2][1] in can_go:
        hang.append('l')

    if len(hang)==0:
        if dirn == 0:
            dirn = 3 
        else:
            dirn -= 1
        prior_action = 'r'
        return 'r'

    action = random.sample(hang,1)[0]

    if action == 'r':
        if dirn == 0:
            dirn = 3 
        else:
            dirn -= 1

    elif action == 'l':
        if dirn == 3:
            dirn = 0
        else:
            dirn += 1
    prior_action = action
    return action
                 
def get_view(data):
    # scan 5-by-5 wintow around current location
    view = [[' ',' ',' ',' ',' ']for _ in range(5)]
    n = 0   
    for i in range(5):
       for j in range(5):             
         if not( i == 2 and j == 2 ):               
             view[i][j] = data[n]
             n += 1
    return view


def print_view( view ):
    print("\n+-----+")
    for i in range(5):
        print("|",end = '')
        for j in range(5):
            if i == 2 and j == 2 :
               print('^',end='')
            else: 
               print( str(view[i][j]),end='' )       
        print("|")     
    print("+-----+")


def record_to_world(view): #save the view into the world[][] which is world model
##EAST   = 0;
##NORTH  = 1;
##WEST   = 2;
##SOUTH  = 3;
    global world
    global colum
    global row
    if dirn == 1:
        c = -2
        r = 0
        colum -= 1
    elif dirn == 3:
        c = 2
        r = 0
        colum += 1
    elif dirn == 2:
        c = 0
        r = -2
        row -= 1
    elif dirn == 0:
        c = 0
        r = 2
        row += 1  
    for i in range(-2,3):
        if c == -2:
            world[colum + c][row + i] = view[0][2+i]
        elif c == 2:
            world[colum + c][row - i] = view[0][2+i]
        elif r == -2 :
            world[colum - i][row + r] = view[0][2+i]
        elif r == 2:
            world[colum + i][row + r] = view[0][2+i]

HOST = 'localhost'
PORT = 31415
ADDR = (HOST, PORT) 

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(ADDR)
data = get_view(sock.recv(24,MSG_WAITALL).decode("UTF-8"))
for i in range(-2,3):
    for j in range(-2,3):
            world[colum - i][row - j] = data[i+2][2+j]

while True:
    if prior_action == 'f':
        record_to_world(data)
    action = hang_out(data)
    sock.send(action.encode("UTF-8"))
    data = get_view(sock.recv(24,MSG_WAITALL).decode("UTF-8"))
  # print_view(data)


