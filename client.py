import socket, threading, sys
from utils import *

defaultconfig = input("use default config?\\nHOST=luna.hackclub.app\nPORT=7171\n[Y/n]> ").lower().strip()
if defaultconfig == "n":
    HOST = input("input server ip here: ")
    PORT = int(input("input port: "))
else:
    HOST = 'luna.hackclub.app'
    PORT = 7171



def receive(sock: socket.socket) -> None:
    try:
        while True:
            try:
                message = sock.recv(1024).decode()
            except Exception as e:
                print(f"[CLIENT] error receiving message {e}")
                break
            print(f"{message}\n")
    finally:
            print("[CLIENT] error while listening for messages. please reconnect")


def startclient() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((HOST, PORT))
        except Exception as e:
            print(f"[CLIENT] connection error: {e}")
            print(f"[CLIENT]: quitting...")
            sys.exit()

        while True:
            username = input("[CLIENT] username: ").strip()
            if username in disallowedusernames:
                print(f"[CLIENT] username {username} disallowed.")
                continue
            break
        
        try:
            client.send(username.encode())
        except:
            print(f"[CLIENT] error sending data to server. please reconnect")
            print("[CLIENT] quitting...")
            sys.exit()

        print(f"joined as {username}")

        listener = threading.Thread(target=receive, args=(client,), daemon=True)
        listener.start()

        while True:
            message = input()

            if message.lower() == 'exit':
                break

            try:
                client.send(f"{message}".encode())
            except Exception as e:
                print(f"[CLIENT] error sending message: {e}")
                break

        # exit sequence
        print("[CLIENT] quitting...")
        listener.join()
        sys.exit()
            
startclient()