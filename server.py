
import socket
from  threading import Thread
import time

SERVER = None
PORT = None
IP_ADDRESS = None

CLIENTS = {}
player_names = []


def handleClient(player_socket, player_name):
    global CLIENTS
    global player_names

    player_type = CLIENTS[player_name]['player_type']

    if(player_type == 'player1'):
        CLIENTS[player_name]['turn'] = True
        player_socket.send(str({'player_type': CLIENTS[player_name]['player_type'], 'turn':CLIENTS[player_name]['turn'],'player_name': player_name }).encode('utf=8'))
    else:
        CLIENTS[player_name]['turn'] = False
        player_socket.send(str({'player_type': CLIENTS[player_name]['player_type'], 'turn':CLIENTS[player_name]['turn'],'player_name': player_name }).encode('utf=8'))

    player_names.append({'name': player_name, 'type': CLIENTS[player_name]['player_type']})
    time.sleep(2)
    if(len(player_names)> 0 and len(player_names)<= 2):
        for c in CLIENTS:
            cSocket = CLIENTS[c]['player_socket']
            cSocket.send(str({'player_names': player_names}).encode('utf-8'))

    while True:
        try:
            message = player_socket.recv(2048)
            print(player_socket)
            print("*****************************")
            print('MESSAGE', message)
            if(message):
                for c in CLIENTS:
                    cSocket = CLIENTS[c][player_socket]
                    cSocket.send(message)
        except:
            pass

def acceptConnections():
    global CLIENTS
    global SERVER

    while True:
        player_socket, addr = SERVER.accept()
        player_name = player_socket.recv(1024).decode().strip()

        if(len(CLIENTS.keys()) == 0):
            CLIENTS[player_name] = {'player_type': 'player1'}
        else:
            CLIENTS[player_name] = {'player_type': 'player2'}
        
        CLIENTS[player_name]['player_socket'] = player_socket
        CLIENTS[player_name]['player_address'] = addr
        CLIENTS[player_name]['player_name'] = player_name
        CLIENTS[player_name]['turn'] = False
        
        print(f"Connection Established With {player_name}: {addr}")
        thread = Thread(target= handleClient, args= (player_socket, player_name))
        thread.start()







def setup():
    print("\n")
    print("\t\t\t\t\t\t*** LUDO LADDER ***")


    global SERVER
    global PORT
    global IP_ADDRESS

    IP_ADDRESS = '127.0.0.1'
    PORT = 5001 # port number shouldn't be less than 1024 reserved ports
    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...")
    print("\n")

    acceptConnections()


setup()
