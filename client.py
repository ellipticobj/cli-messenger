import socket
import threading

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
            print(f"\n{message}")
        except Exception as e:
            print(f"error receiving message {e}")
            break

def startclient() -> None:
    '''
    starts client
    '''
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((HOST, PORT))
            print("connected to the server. start typing below")

            # Start a thread to listen for incoming messages
            threading.Thread(target=receivemessages, args=(client_socket,), daemon=True).start()

            while True:
                message = input("> ")
                if message.lower() == 'exit':
                    print("Disconnecting...")
                    break
                client_socket.send(message.encode())
        except Exception as e:
            print(f"connection error {e}")

if __name__ == "__main__":
    startclient()
