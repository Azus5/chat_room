import curses
import time
import sys
import socket
from threading import Thread
from client_class import Client 

running = True

def reset_screen(stdscr):
  curses.nocbreak()
  stdscr.keypad(False)
  curses.endwin()

def receive(stdscr, client_socket):
  y = 0

  while running:
    try:
      rows, cols = stdscr.getmaxyx()
      msg = client_socket.recv()

      if repr(msg) != '':
        stdscr.insstr(y, 0, msg)
        stdscr.move(rows - 1, len("Digite sua Mensagem: "))
        stdscr.noutrefresh()
        curses.doupdate()
        y+=1
    except OSError:
      break
  reset_screen(stdscr)

def getInput(stdscr, client_socket):
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
      if user_input == curses.KEY_BACKSPACE or user_input == '\x7f': 
        msg = msg[:-1]

      stdscr.addstr(rows - 1, len("Digite sua Mensagem: "), msg)
    client_socket.send(msg)
  
  running = False
  client_socket.close()
  reset_screen(stdscr)

if __name__ == "__main__":
  HOST = "192.168.0.112"
  PORT = 12397
  client_socket = Client(HOST)
  client_socket.connect()
  client_socket.send(input("Username: "))

  stdscr = curses.initscr()
  curses.cbreak()
  stdscr.keypad(True)
  stdscr.scrollok(True)
  stdscr.clear()
  receive_thread = Thread(target=receive, args=[stdscr, client_socket])
  user_input = Thread(target=getInput, args=[stdscr, client_socket])
  receive_thread.start()
  user_input.start()