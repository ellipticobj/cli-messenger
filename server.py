import socket
import threading
from datetime import datetime
import sys

class Server:
    def __init__(self, host='0.0.0.0', port=7171):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.clients = {} # dictionary of socket: username
        self.running = True

        self.whitelist = {} # set of whitelisted users
        self.blacklist = {} # set

        self.whitelistenabled = False # enables/disables whitelist (ONLY allows list of allowed users)
        self.blacklistenabled = False # enables/disables blacklist (allows everyone EXCEPT disallowed users)

        self.profanityfilter = 'off' # off, block, censor
        self.profanitywords = set([]) # add blocked words here

        self.setup()

    def setup(self):
        '''sets up the server'''
        if self.whitelistenabled and self.blacklistenabled:
            print("both whitelist and blacklist cannot be enabled at the same time")
            sys.exit()

        self.server.bind((self.host, self.port))
        self.server.listen()
        self.log(f"server listening at {self.host}:{self.port}")

    def log(self, message):
        '''prints a log + stores it in a log file'''
        logfile = "server.log"
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entr = f"[{now}] {message}"
        print(entr)
        with open(logfile, "a") as file:
            file.write(f"{entr}\n")

    def handleclient(self, clsock):
        '''handles client connection'''
        username = clsock.recv(1024).decode()

        if self.validate(username):
            self.clients[clsock] = username
            self.broadcast(f"{username} joined")
        else:
            clsock.send("connection rejected")
            clsock.close()
            return

        try:
            while self.running:
                message = clsock.recv(1024).decode()
                if not message:
                    break
                self.procmessage(username, message)
        except:
            pass

        del self.clients[clsock]
        self.broadcast(f"{username} has left the chat!")
        clsock.close()

    def procmessage(self, username, message):
        '''handles messages'''
        if message.startswith('/'):
            pass

        if self.profanityfilter:
            message = self.filter(message)

        if message:
            self.broadcast(f"{username}: {message}")

    def filter(self, message):
        words = message.split()
        for i, word in enumerate(words):
            if word.lower() in self.profanitywords:
                if self.profanityfilter == "block":
                    return None
                elif self.profanityfilter == "censor":
                    words[i] = "*" * len(word)
        return " ".join(words)

    def validate(self, username):
        # TODO: change username check to ip check
        '''
        checks if client's ip is black/whitelisted
        returns true if user is allowed to connect, falso if disallowed
        '''
        if self.whitelistenabled:
            if username in self.whitelist:
                return True
            else:
                return False
        if self.blacklistenabled:
            if username in self.blacklist:
                return False
            else:
                return True

    def broadcast(self, message):
        for client in self.clients:
            try:
                self.log(message)
                client.send(message.encode())
            except Exception as e:
                self.log(f"failed to send message to {client} due to {e}")

    def shutdown(self):
        # TODO
        pass

def run():
    try:
        server = Server()

        acceptthread = threading.Thread(target = lambda: [server.handleclient(client) for client in iter(lambda: server.server.accept()[0], None)], daemon=True)
        acceptthread.start()
    except KeyboardInterrupt:
        print("quitting server")
    finally:
        server.shutdown()


if __name__ == "__main__":
    print("starting server")
    run()


print("server quit")
