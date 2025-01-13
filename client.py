import socket
import threading


HOST = input("input your server ip here: ")
PORT = 5000

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
                message: str = input("> ")
                if message.lower() == 'exit':
                    print("Disconnecting...")
                    break
                client_socket.send(message.encode())
        except Exception as e:
            print(f"connection error {e}")

if __name__ == "__main__":
    startclient()
