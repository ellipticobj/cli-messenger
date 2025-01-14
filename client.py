import socket
import threading
from utils import *

choice = input("do you want to use default server config?\nHOST=luna.hackclub.app\nPORT=7171\n[Y/n]> ").lower().strip()
if choice == "n":
    HOST = input("input server ip here: ")
    PORT = input("input port: ")
else:
    HOST = 'luna.hackclub.app'
    PORT = 7171


def receivemessages(sock: socket.socket) -> None:
    """
    receives messages and prints them
    """
    while True:
        try:
            message = sock.recv(1024).decode()
            print(f"\n{message}\n")
        except Exception as e:
            print(f"error receiving message {e}")
            break

def startclient() -> None:
    '''
    starts client
    '''
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((HOST, PORT))
            while True:
                username = input("[SYS]: username: ").strip()
                if username in disallowedusernames:
                    print(f"[SYS]: username disallowed.")
                    continue
                client.send(username.encode())
                break

            print("joined the chat.")

            # Start a thread to listen for incoming messages
            threading.Thread(target=receivemessages, args=(client,), daemon=True).start()

            while True:
                message = input("> ")
                if message.lower() == 'exit':
                    print("disconnecting...")
                    break
                client.send(message.encode())
        except Exception as e:
            print(f"connection error {e}")


startclient()
