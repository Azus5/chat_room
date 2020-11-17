import socket
from threading import Thread

# Accept connection outside localhost
HOST = ''
PORT = 12397
BUFFER_SIZE = 1024
clients = {}
addresses = {}

def accept_connections():
  """Wait for incoming connections"""

  while True:
    client, client_address = server_socket.accept()
    print("%s: Entered the chat!" % client_address[0])
    client.send(bytes("Type your message, and press enter (quit! to exit), ", "utf-8"))
    addresses[client] = client_address

    # For each client, create a thread to handle him
    Thread(target=handle_client,  args=(client,)).start()

def handle_client(client):
  """Handle client connection"""
  name = client.recv(BUFFER_SIZE).decode("utf-8")
  client.send(bytes("Welcome %s" % name, "utf-8"))
  broadcast(bytes("%s entered the chat", "utf-8"))
  clients[client] = name

  while True:
    msg = client.recv(BUFFER_SIZE)
    if (msg != bytes("quit!", "utf-8")):
      broadcast(msg, name+": ")
    else:
      client.send(bytes("quit!", "utf-8"))
      client.close()
      del clients[client]
      broadcast(bytes("%s: exit the chat" % name, "utf-8"))
      break

def broadcast(msg, prefix=""):
  for client in clients:
    client.send(bytes(prefix, "utf-8") + msg)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Destroy socket if the connection is iterrupted
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((HOST, PORT))

if __name__ == "__main__":
  server_socket.listen(5)
  print("Waiting for connections...")
  ACCEPT_THREAD = Thread(target=accept_connections)
  ACCEPT_THREAD.start()
  ACCEPT_THREAD.join()
  server_socket.close()