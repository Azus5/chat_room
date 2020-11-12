import socket
from threading import Thread

HOST = input("Your host: ")
PORT = 12397
BUFFER_SIZE = 1024

def receive():
  name = bytes(input("Seu usuario: "), "utf-8")
  client_socket.send(name)
  user_thread.start()

  while True:
    try:
      msg = client_socket.recv(BUFFER_SIZE).decode("utf-8")
      print(msg)

    except OSError:
      break

def send():
  msg = ""
  while(msg != "quit!"):
    msg = input("Digite sua mensagem: ")
    client_socket.send(bytes(msg, "utf-8"))
    if(msg == "quit!"): client_socket.close()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

user_thread = Thread(target=send)
receive_thread = Thread(target=receive)
receive_thread.start()