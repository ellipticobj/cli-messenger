import socket
import threading
import time
from datetime import datetime
from typing import _P

from client import Client

class Server:
    def __init__(self, host='0.0.0.0', port=7171):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.clients = {} # dictionary of socket: username
        self.running = True

        self.whitelistenabled = False
        self.blacklistenabled = False
        self.whitelist = {} # set of whitelisted users
        self.blacklist = {} # set
        self.whitelist = False
        self.blacklist = False
        self.profanity_filter = "off"
        self.profanity_words = set(['badword1', 'badword2'])

        # self.setup() TODO

    def setup(self):
        '''sets up the server'''
        pass

    def log(self, message):
        '''prints a log + stores it in a log file'''
        pass

    def handleclient(self, clsock):
        '''handles client connection'''
        pass

    def validatecl(self, clip):
        '''checks if client's ip is black/whitelisted'''
        pass

    def broadcast(self, message):
        for client in self.clients:
            try:
                client.send(message.encode())
            except Exception as e:
                self.log(f"failed to send message to {client} due to {e}")

if __name__ == "__main__":
    server = Server()

    acceptthread = threading.Thread(target = lambda: [server.handleclient(client) for client in iter(lambda: server.server.accept()[0], None)], daemon=True)
    acceptthread.start()

    print(f"server started at {server.host}:{server.port}")
