import socket
import threading
import time
from datetime import datetime

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
