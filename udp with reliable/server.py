import socket
import ast
from _thread import *

players = []
host, port = '127.0.0.3', 1234

ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    ServerSocket.bind((host, port))
    print('Сервер в сети!')
except socket.error as e:
    print(str(e))

ThreadCount = -1

def threaded_client():
    global players, ThreadCount
    
    while True:
        data, addr = ServerSocket.recvfrom(20480)
        try:
            log = ast.literal_eval(data.decode('utf-8'))
            
            if 'new_connection' in log:
                ThreadCount += 1
                client_id = ThreadCount
                players.append({'id': client_id})
                ServerSocket.sendto(str.encode(str(client_id)), addr)
                print(f'New connection from {addr}, assigned ID: {client_id}')
                continue
            
            if log != None and 'id' in log:
                player_id = log['id']
                if 0 <= player_id < len(players):
                    players[player_id] = log

            pack = str(players)
            ServerSocket.sendto(str.encode(pack), addr)
            
        except (ValueError, SyntaxError) as e:
            print(f"Error decoding data from {addr}: {e}")

start_new_thread(threaded_client, ())

while True:
    pass

ServerSocket.close()
