import socket
import ast
from _thread import *
import pygame, sys

def socket_thread():
    global client_id, players, x, y
    ClientSocket.sendto(str.encode(str({'new_connection': True})), (host, port))
    data, _ = ClientSocket.recvfrom(20480)
    client_id = int(data.decode('utf-8'))
    print(f"Connected to server. Assigned ID: {client_id}")
    while True:
        pack = str({'id': client_id,
                          'x': x,
                          'y': y,
                        })
        ClientSocket.sendto(str.encode(pack), (host, port))
        data, _ = ClientSocket.recvfrom(20480)
        players = ast.literal_eval(data.decode('utf-8'))

        
ClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = '127.0.0.3'
port = 1234
print('Connecting to server...')

client_id = None
players = []

FPS = 60

pygame.init()
sc = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()


x, y = 0, 0
start_new_thread(socket_thread, ())

speed = 3
while True:
    sc.fill('black')
    clock.tick(FPS)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]: y -= speed
    if keys[pygame.K_a]: x -= speed
    if keys[pygame.K_s]: y += speed
    if keys[pygame.K_d]: x += speed

    for player in players:
        if player['id'] == client_id:
            pygame.draw.rect(sc, 'blue', (player['x'], player['y'], 20, 20))
        else:
            pygame.draw.rect(sc, 'red', (player['x'], player['y'], 20, 20))
    

    pygame.display.update()
    
