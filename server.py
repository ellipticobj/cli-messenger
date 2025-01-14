import socket
import threading
from typing import Dict, Tuple
from utils import *

HOST = '0.0.0.0'
PORT = 7171

clients: Dict[socket.socket, str] = {}

def broadcast(message: bytes, sender: socket.socket = "") -> None:
    '''
    broadcasts a message
    '''
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode())
            except Exception as e:
                print(f"[SERVER] error sending message {e}")
                client.close()
                del clients[client]


def handleclient(client: socket.socket, addr: Tuple[str, int]) -> None:
    '''
    handles communication
    '''

    # username handling
    username = client.recv(1024).decode().strip()
    clients[client] = username
    print(f"{username} joined from {addr}")
    broadcast(f"[SYS]: {username} joined")

    # message handling
    try:
        while True:
            username, message = client.recv(1024)
            if not message:
                break
            broadcast(message, client)
            print(f"{username} sent message: {message}")
    except Exception as e:
        print(f"[SERVER] error while handling messages: {e}")

    # cleanup after error
    finally:
        username = clients.pop(client, "unknown user")
        broadcast(f"{username} disconnected", )
        print(f"(from {addr})")
        client.close()
        del clients[client]
    client.close()
    del clients[client]
    

def startserver() -> None:
    '''
    starts the server (duh)
    '''
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"server started on {HOST}:{PORT}")
        
        while True:
            client, addr = server.accept()
            print()
            threading.Thread(target=handleclient, args=(client,addr), daemon=True).start()

input("start server: ")
print("starting server")
print()
startserver()