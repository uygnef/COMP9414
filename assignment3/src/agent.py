import socket

HOST = 'localhost'
PORT = 8080
ADDR = (HOST, PORT) 

sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
sock.connect(ADDR)

def get_view(data):
    # scan 5-by-5 wintow around current location
    view = [[[' ']for _ in range(5)]for _ in range(5)]
    if len(data) > 24:
        for i in range(5):
           for j in range(5):             
             if not( i == 2 and j == 2 ):               
                 view[i][j] = str(data.read(1))
    return view


def print_view( view ):
    print("\n+-----+")
    for i in range(5):
        print("|")
        for j in range(5):
            if i == 2 and j == 2 :
               print('^',end='')
            else: 
               print( str(view[i][j]),end='' )       
        print("|")
      
    print("+-----+")



while True:
    data = sock.recv(24).decode() 
    view = get_view(data)
    print_view( view )
    action = input("dirtion:")
    sock.send(action.encode())

    
