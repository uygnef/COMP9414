
from socket import *

dirn = 3
world = [['' for _ in range(80)]for _ in range(80)]
row = 40
colum = 40
stone = False

def hang_out(view):
    global dirn
    global stone
    if view[1][2] == ' ' or view[1][2] == 'o':
        if view[1][2] == 'o':
            stone = True
        action = 'f'
        record_to_world()
    elif view[2][3] == ' ' or view[2][3]== 'o' :
        action = 'r'
        if dirn - 1 < 0:
            dirn = 3 
        else:
            dirn -= 1
    else: 
        action = 'l'
        if dirn + 1 > 3:
            dirn = 0
        else:
            dirn += 1
    return action
                 
def get_view(data):
    # scan 5-by-5 wintow around current location
    global view
    view = [[' ',' ',' ',' ',' ']for _ in range(5)]
    print(len(data))
    n = 0

    while len(data) < 24:
        a = 's'
        sock.send(a.encode())
        data = sock.recv(24).decode()
        print(len(data))
    
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


def record_to_world(): #save the view into the world[][] which is world model
##EAST   = 0;
##NORTH  = 1;
##WEST   = 2;
##SOUTH  = 3;
 global world
 global colum
 global row
 if dirn == 1:
     c = -3
     r = 0
 elif dirn == 3:
     c = 3
     r = 0
 elif dirn == 2:
     c = 0
     r = -3
 elif dirn == 0:
     c = 0
     r = 3	

 if r == 0:
     colum = colum + c
     print(dirn , colum ,c)
 if c == 0:
     row += r 
	
 for i in range(-2,3):
    if r == 0:
        world[colum][row+i] = view[0][2+i]
        print(world[colum][row+i])
    if c == 0:
        world[colum + i][row] = view[0][2+i]
        print(world[colum + i][row])


HOST = 'localhost'
PORT = 31415
ADDR = (HOST, PORT) 

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(ADDR)
a = 0
while True:
    a = 0
    data = sock.recv(1024)
    data = get_view(sock.recv(1024).decode("UTF-8"))
    print_view(data)
    sock.send(hang_out(data).encode("UTF-8"))
##    if len(data)>23:
##        for i in range(5):
##            for j in range(5):
##                if i !=2 or j != 2:
##                    print(data[a],end='')
##                    a += 1
##                else:
##                    print('^',end='')
##            print()
    print()


    
