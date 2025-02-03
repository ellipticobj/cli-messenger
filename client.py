import socket
import threading
import curses
from curses import wrapper
from datetime import datetime

class Client:
    def __init__(self, stdscr):
        '''
        :3
        '''
        self.stdscr = stdscr
        self.running = True
        self.host = "luna.hackclub.app"
        self.port = 7171
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = "anonymous"
        self.setupui()

    def setupui(self):
        '''
        initializes the windows for the chat and input for persistant prompts
        '''
        curses.curs_set(1)
        self.stdscr.nodelay(1)
        self.stdscr.timeout(100)

        self.rows, self.cols = self.stdscr.getmaxyx()

        self.inputwin = curses.newwin(1, self.cols, self.rows-1, 0)
        self.chatwin = curses.newwin(self.rows-1, self.cols, 0, 0)
        self.chatwin.scrollok(True)

    def display(self, message):
        '''
        prints a message
        '''
        try:
            timestamp = datetime.now().strftime("%H:%M")
            self.chatwin.addstr(f"[{timestamp}] {message}\n")
            self.chatwin.refresh()
        except:
            pass

    def getusrname(self):
        '''
        sets user username
        '''
        prompt = "> "
        usrnamewin = curses.newwin(3, 50, 5, 5)

        usrnamewin.addstr(0, 0, f"enter username (leave empty for anon)\n{prompt}")
        usrnamewin.refresh()

        curses.echo()
        username = usrnamewin.getstr(1, len(prompt), 20).decode()
        curses.noecho()

        usrnamewin.erase()
        self.stdscr.touchwin()
        self.stdscr.refresh()

        self.username = username.strip() if username.strip() else "anon"

    def connect(self):
        '''
        attempts to connect to server with username
        '''
        self.getusrname()

        try:
            # attempts to connect to server
            # timeout set to 5 seconds
            self.client.settimeout(5)
            self.client.connect((self.host, self.port))
            self.client.send(self.username.encode())

            response = self.client.recv(1024).decode()
            if response.lower() == "connection rejected":
                raise ConnectionError("connection rejected")

            self.client.settimeout(None)
            return True

        except Exception as e:
            self.display(f"connection failed, error occured.\n{e}")
            self.running = False
            return False

    def receiveloop(self):
        '''
        receive messages from server
        '''
        while self.running:
            try:
                message = self.client.recv(1024).decode()
                if not message:
                    raise ConnectionError("server disconnection")

                self.display(message)
            except Exception as e:
                self.display(f"error occured in receiveloop: {e}\n exiting...")
                self.running = False
                break

    def inputloop(self):
        '''
        receive user input (messages)
        '''
        buf = ''

        while self.running:
            try:
                self.inputwin.clear()
                self.inputwin.addstr(0, 0, "> " + buf)
                self.inputwin.refresh()

                key = self.inputwin.getch()

                if key == curses.KEY_ENTER or key in [10, 13]:
                    if buf.strip():
                        try:
                            self.client.settimeout(5)
                            self.client.send(buf.encode())
                            buf = ''
                        except socket.timeout:
                            self.display("server has not responded for 5 seconds. disconnecting")
                            self.running = False
                            break
                        except Exception as e:
                            self.display(f"error sending message: {e}")
                            self.running = False
                            break
                        finally:
                            self.client.settimeout(None)

                elif key == curses.KEY_BACKSPACE or key == 127:
                    buf = buf[:-1]
                elif 0 <= key < 256:
                    buf += chr(key)

            except Exception as e:
                # pass
                self.display(f"error occured in inputloop: {e}")
                self.running = False

    def run(self):
        '''
        runs the app (duh)
        '''
        if not self.connect():
            return

        receivethread = threading.Thread(target=self.receiveloop, daemon=True)
        receivethread.start()

        self.inputloop()
        self.client.close()
        curses.endwin()
        print("disconnected")

def main(stdscr):
    client = Client(stdscr)
    client.run()

if __name__ == "__main__":
    wrapper(main)
