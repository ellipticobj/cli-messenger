import socket
import threading
from typing import Dict, Tuple
from utils import *

HOST = '0.0.0.0'
PORT = 7171

clients: Dict[socket.socket, str] = {}

def broadcast(message: bytes, sender: socket.socket) -> None:
    '''
    broadcasts a message
    '''
    
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode())
            except Exception as e:
                print(f"error sending message {e}")
                client.close()
                del clients[client]


def handleclient(client: socket.socket, addr: Tuple[str, int]) -> None:
    '''
    handles communication
    '''

    try:
        # username handling
        while True:
            client.send("[SYS]: username: ".encode())
            username = client.recv(1024).decode().strip()
            if username in disallowedusernames:
                client.send("[SYS]: username disallowed.")
                continue
            clients[client] = username
            break
        print(f"{username} joined from {addr}")
        broadcast(f"[SYS]: {username} joined")

        while True:
            message = client.recv(1024)
            if not message:
                break
            broadcast(message, client)
        print(f"{client} sent message: {message}")
    except Exception as e:
        print(f"client error: {e}")
    finally:
        username = clients.pop(client, "unknown user")
        broadcast(f"{username} disconnected")
        print(f"{username} disconnected (from {addr})")
        client.close()
    
    print(f"{client} disconnected")
    clients.remove(client)
    client.close()
    

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
            print(f"new connection from {addr}")
            clients.append(client)
            threading.Thread(target=handleclient, args=(client,), daemon=True).start()

input("start server: ")
print("starting server")
print()
startserver()