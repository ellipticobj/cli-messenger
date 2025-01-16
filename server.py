import socket, threading
from typing import Dict, Tuple
from utils import *

HOST = '0.0.0.0'
PORT = 7171

clients: Dict[socket.socket, str] = {}

def broadcast(message: bytes, sender: socket.socket = "") -> None:
    for client in list(clients.keys()):
        try:
            if client != sender:
                client.send(f"{message}".encode())
        except Exception as e:
            print(f"[SERVER] error broadcasting message {e}")
            client.close()
            del clients[client]

def handleclient(client: socket.socket, addr: tuple[str, int]) -> None:
    try:
        username = client.recv(1024).decode()
        clients[client] = username
    except Exception as e:
        print(f"[SERVER] error receiving/setting username")
        client.close()
        del clients[client]

    print(f"{username} joined from {addr}")
    broadcast(f"[SERVER] {username} joined")

    while True:
        try:
            message = client.recv(1024).decode()
            print(f"{username}: {message}")
        except Exception as e:
            print(f"[SERVER] error receiving message")
            client.close()
            del clients[client]

        broadcast(f"{username}: {message}", sender=client)

    
def startserver() -> None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
            server.bind((HOST, PORT))
            server.listen()

            print(f"server started on {HOST}:{PORT}")

            while True:
                client, addr = server.accept()
                threading.Thread(target=handleclient, args=(client, addr), daemon=True).start()
    except KeyboardInterrupt:
        print(f"shutdown starting")

        for client in list(clients.keys()):
            print(f"informing client that server is shutting down")
            broadcast(f"[SERVER] shutting down...")
            print(f"closing connection with {clients[client]}")
            client.close()
            print(f"removing {clients[client]} from online clients")
            del clients[client]
            print(f"done")
            print()
        print(f"server shutting down")


# # TODO: add support for custom ip and port
# # TODO: add system commands, sending messages, etc
# # input("start server: ")
print("starting server")
print()
startserver()