import socket
import threading
import curses
from curses import wrapper
from datetime import datetime

class Client:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.running = True
        self.host = "luna.hackclub.app"
        self.port = 7171
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = "anonymous"

    def setupui(self):
        curses.curs_set(1)
        self.stdscr.nodelay(1)
        self.stdscr.timeout(100)

        self.rows, self.cols = self.stdscr.getmaxyx()

        self.inputwin = curses.newwin(1, self.cols, self,rows-1, 0)
        self.chatwin = curses.newwin(self.rows-1, self.cols, 0, 0)
        self.chatwin.scrollok(True)

    def display(self):
        timestamp = datetime.now().strftime("%H:%M")
        self.chatwin.addstr(f"[{timestamp}] {message}\n")
        self.chatwin.refresh()

    def getusrname(self):
        self.stdscr.addstr(0, 0, "enter username: ")
        self.stdscr.refresh()
        curses.echo()

        self.username = self.stdscr.getstr(0, 15, 20).decode()
        curses.noecho()
        self.stdscr.clear()

    def connect(self):
        self.getusrname()

        try:
            self.client.connect((self.host, self.port))
            self.client.send(self.username.encode())
            response = self.client.recv(1024).decode()

            if response == "connection rejected":
                self.display("connect rejected by server")
                self.running = False
                return False
            return True

        except Exception as e:
            self.display(f"connection failed, error occured.\n{e}")
            self.running = False
            return False
