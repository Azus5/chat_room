import curses
import time
import sys
import socket
from threading import Thread

HOST = "192.168.0.112"
# HOST = "127.0.0.1"
PORT = 12397
BUFFER_SIZE = 1024
running = True
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
client_socket.send(bytes(sys.argv[1], "utf-8"))

def reset_screen(stdscr):
  curses.nocbreak()
  stdscr.keypad(False)
  curses.endwin()

def receive(stdscr: curses.initscr()):
  y = 0

  while running:
    try:
      rows, cols = stdscr.getmaxyx()
      msg = client_socket.recv(BUFFER_SIZE).decode("utf-8")
      
      if y == rows - 5: stdscr.scroll(5)
      
      if repr(msg) != '':
        stdscr.insstr(y, 0, msg)
        stdscr.move(rows - 1, len("Digite sua Mensagem: "))
        stdscr.noutrefresh()
        curses.doupdate()
        y+=1
    except OSError:
      break
  reset_screen(stdscr)

def getInput(stdscr: curses.initscr()):
  msg = ""
  user_input = ''

  while msg != "quit!":
    rows, cols = stdscr.getmaxyx()
    stdscr.addstr(rows - 1, 0, "Digite sua Mensagem: ")

    msg = ""
    user_input = ''
    while True:
      rows, cols = stdscr.getmaxyx()
      stdscr.noutrefresh()
      curses.doupdate()
      stdscr.clrtoeol()
      user_input = stdscr.get_wch()
      if user_input == '\n':
        break
      if isinstance(user_input, str) and user_input.isprintable():
        msg += user_input
      if user_input == curses.KEY_BACKSPACE or user_input == '\x7f': msg = msg[:-1]

      stdscr.addstr(rows - 1, len("Digite sua Mensagem: "), msg)

    
    client_socket.send(bytes(msg, "utf-8"))
  
  running = False
  client_socket.close()
  reset_screen(stdscr)

if __name__ == "__main__":
  stdscr = curses.initscr()
  curses.cbreak()
  # curses.noecho()
  stdscr.keypad(True)
  stdscr.scrollok(True)
  stdscr.clear()
  receive_thread = Thread(target=receive, args=[stdscr])
  user_input = Thread(target=getInput, args=[stdscr])
  receive_thread.start()
  user_input.start()