import socket
import threading

HOST = '0.0.0.0'
PORT = 5000

clients = []

def broadcast(message: bytes, sender: socket.socket) -> None:
    '''
    broadcasts a message
    '''
    
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except Exception as e:
                print(f"error sending message {e}")
                client.close()
                clients.remove(client)


def handleclient(clientsock: socket.socket) -> None:
    '''
    handles communication
    '''
    
    while True:
        try:
            message = clientsock.recv(1024)
            if not message:
                break
            broadcast(message, clientsock)
        except Exception as e:
            print(f"client error: {e}")
            break
    
    print("disconnected")
    clients.remove(clientsock)
    clientsock.close()


def startserver() -> None:
    '''
    starts the server (duh)
    '''
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SQL_SOCKET, socket.SO_REUSEADDR, 1)
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