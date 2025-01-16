import socket
import threading
from utils import *

choice = input("do you want to use default server config?\nHOST=luna.hackclub.app\nPORT=7171\n[Y/n]> ").lower().strip()
if choice == "n":
    HOST = input("input server ip here: ")
    PORT = int(input("input port: "))
else:
    HOST = 'luna.hackclub.app'
    PORT = 7171

serverrunning = True

def receiveprivmessages(sock: socket.socket) -> None:
    global serverrunning
    try:
        while serverrunning:
            try:
                message = sock.recv(1024).decode()

                # only reads private messages
                if message.startswith("PRIVATE:"):
                    content = message[8:]
                    if content == 'quitserver':
                        print(f"[CLIENT] server has shut down. exiting...")
                        serverrunning = False
                        break

            except Exception as e:
                print(f"[CLIENT] error at receivesysmessages {e}")
                break
    finally:
        print(f"[CLIENT] private thread closed. please reconnect")

def receivemessages(sock: socket.socket) -> None:
    """
    receives messages and prints them
    """
    global serverrunning
    consecmessage = 0
    prevmessage = ""
    try:
        # buffer = ""
        while serverrunning:
            try:
                message = sock.recv(1024).decode()
                # buffer += data
                # while "\n" in buffer:
                #     message, buffer = buffer.split("\n", 1)

                    # makes sure the message is a public message
                if message.startswith("PUBLIC:"):
                    # spam protection to prevent massive cpu usage
                    if message == prevmessage:
                        if consecmessage >= 20:
                            print(f"[CLIENT] more than 20 identical messages received, looks like the server is down. ")
                            print(f"[CLIENT] blocked incoming messages just to be safe. if you think this is an error, reconnect again :3")
                            print(f"[CLIENT] press control+c to exit")
                            serverrunning = False
                        consecmessage += 1
                    prevmessage = message

                    print(f"\n{message[8:]}\n", end="")
            except Exception as e:
                print(f"[CLIENT] error receiving message {e}")
                break
    finally:
        print("[CLIENT] Public message thread closed. please reconnect")

def startclient() -> None:
    '''
    starts client
    '''
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((HOST, PORT))
            client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Disable Nagle's algorithm
            while True:
                # username
                username = input("[CLIENT] username: ").strip()
                if username in disallowedusernames:
                    print(f"[CLIENT] username disallowed.")
                    continue
                client.send(username.encode())
                break
            
            print(f"you joined the chat as {username}")
        except Exception as e:
            print(f"[CLIENT] connection error: {e}")
            print(f"[CLIENT] exiting...")
            return
        
        try:
            # listen for incoming messages
            pubthread = threading.Thread(target=receivemessages, args=(client,), daemon=True)
            privthread = threading.Thread(target=receiveprivmessages, args=(client,), daemon=True)

            pubthread.start()
            privthread.start()

            prevmessage = ""
            consecmessage = 0

            while serverrunning:
                message = input("")
                if message == prevmessage:
                    if consecmessage >= 10:
                        print(f"[CLIENT] more than 10 identical messages sent. ")
                        print(f"[CLIENT] you have been kicked for spamming >:(")
                        message = 'exit'
                    consecmessage += 1
                prevmessage = message
                if message.lower() == 'exit':
                    print("disconnecting...")
                    break
                client.send(f"{message}\n".encode())
            
            pubthread.join()
            privthread.join()
        except Exception as e:
            print(f"[CLIENT] error while sending message {e}")


startclient()
