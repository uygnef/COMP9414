import random
from socket import *

dirn = 3
world = [[None for _ in range(80)]for _ in range(80)]
row = 40
colum = 40
stone = False
prior_action = None
have_been = set((colum,row))
can_go = [' ','o']
axo = False
gold = False
key = False

class Node():
    def __init__(self):
        self.value = None
        self.father = None
        self.stone = False
        self.colum = None
        self.row = None
        
def search_path(end_colmn,end_row): #use breadth first search to find the right position
    global colum
    global row
    global stone
    global axo
    global gold
    
    start = Node()
    start.colum = colum
    start.row = row
    start.stone = stone
    possibal_path = [start]
    have_been = [(colum,row)]
    for node in possibal_path:
        can_go = [' ','o','k','a','g']
        if node.colum == end_colmn and node.row == end_row:            
            break
        if node.stone:
            can_go =  can_go + ['~']
        if axo:
            can_go = can_go + ['T']
        if key:
            can_go = can_go + ['k']
        for i in [-1,1]:                     #breadth frist search check out every place where can go to
            if world[node.colum+i][node.row] in can_go:
                new_node = Node()
                new_node.father = node
                new_node.colum = node.colum+i
                new_node.row = node.row
                new_node.stone = node.stone
                if world[node.colum+i][node.row] == '~':
                    new_node.stone = False
                if (new_node.colum,new_node.row) not in have_been:
                    have_been.append((new_node.colum,new_node.row))
                    possibal_path.append(new_node)

            if world[node.colum][node.row+i] in can_go:
                new_node = Node()
                new_node.father = node
                new_node.colum = node.colum
                new_node.row = node.row+i
                new_node.stone = node.stone
                if world[node.colum][node.row+i] == '~':
                    new_node.stone = False
                if (new_node.colum,new_node.row) not in have_been:
                    have_been.append((new_node.colum,new_node.row))
                    possibal_path.append(new_node)
    if node.colum != end_colmn or node.row != end_row: #search all possibal path can not get goal
        return False
    result = []
    while node.father != None:
        result.append([node.colum,node.row])       
        node = node.father
    return result 
    

def go_to(end):
    global dirn
    global prior_action
    global colum
    global row
    print(prior_action)
    a = colum - end[0]
    b = row - end[1]
    print('a={},b={},dirn={}'.format(a,b,dirn))
    print('colum={},row={},end[0]={},end[1]={}'.format(colum,row,end[0],end[1]))
    if a == -1:
        if dirn == 3:
            prior_action = 'f'
            if world[end[0]][end[1]] == 'T':
                return 'c'
            if world[end[0]][end[1]] == '-':
                return 'u'
            return 'f'
    if a == 1:
        if dirn == 1:
            prior_action = 'f'
            if world[end[0]][end[1]] == 'T':
                return 'c'
            if world[end[0]][end[1]] == '-':
                return 'u'
            return 'f'
    if b == 1:
        if dirn == 2:
            prior_action = 'f'
            if world[end[0]][end[1]] == 'T':
                return 'c'
            if world[end[0]][end[1]] == '-':
                return 'u'
            return 'f'
    if b == -1:
        if dirn == 0:
            prior_action = 'f'
            if world[end[0]][end[1]] == 'T':
                return 'c'
            if world[end[0]][end[1]] == '-':
                return 'u'
            return 'f'
    
    if dirn == 0:
        dirn = 3 
    else:
        dirn -= 1
    prior_action = 'r'
    return 'r'
            
            
    

def hang_out(view):
    global dirn
    global stone
    global prior_action
    global can_go
    # find the area that can go but have not been   
    #stack = [] #save the dirction order by the prioritize

    hang = []
    if view[1][2] in can_go:
        for _ in range(6):
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
    if action == 'f' and view[1][2] == 'o':
        stone = True
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

for _ in range(150):
    action = hang_out(data)
    sock.send(action.encode("UTF-8"))
    data = get_view(sock.recv(24,MSG_WAITALL).decode("UTF-8"))
    if prior_action == 'f':
        record_to_world(data)

def target():      #search all item  from world map
    result = {}
    for i in range(30,60):
        for j in range(30,60):
            if world[i][j] == 'k':
                result['k']=(i,j)
            if world[i][j] == 'a':
                result['a']=(i,j)
            if world[i][j]== 'g':
                result['g']=(i,j)
            if world[i][j]== 'o':
                result['o']=(i,j)
    return result
profile={'o':axo,'g':gold,'k':key,'o':stone}
destination = {}
result = target()
for a in result:
    track = search_path(result[a][0],result[a][1]) #all the possibal way to get item
    if track:
        profile[a] = True
        destination[a] = track
        
i = -1
for p in destination:
    path = destination[p]
    while len(path) > 0:
        print(path)
        des = path.pop()
        action = go_to(des)
        sock.send(action.encode("UTF-8"))
        data = get_view(sock.recv(24,MSG_WAITALL).decode("UTF-8"))
        if prior_action == 'f':
            record_to_world(data)
        if des[0] == result[p][0] and des[1] == result[p][1]:
            break
        if prior_action != 'f':
            path.append(des)

    
    
  # print_view(data)


