import socket
import ast
from _thread import *
from reliable_udp import reliable_send_receive  # Импорт нашей функции

def socket_thread():
    global client_id, players
    # Используем надежную отправку для получения ID
    response = reliable_send_receive(ClientSocket, {'new_connection': True}, (host, port))
    if response is None:
        print("Failed to connect to server")
        return
    
    client_id = int(response)
    print(f"Connected to server. Assigned ID: {client_id}")
    
    while True:
        pack = str({'id': client_id})
        ClientSocket.sendto(str.encode(pack), (host, port))
        data, _ = ClientSocket.recvfrom(20480)
        players = ast.literal_eval(data.decode('utf-8'))

ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '127.0.0.3'
port = 1234
print('Connecting to server...')

client_id = None

start_new_thread(socket_thread, ())

while True:
    pass