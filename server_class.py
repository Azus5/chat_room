import socket

class ServerSocket:
  def __init__(self, host, port):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.host = host
    self.port = port
    self.clients = {}
    self.addresses = {}
    self.socket.bind((host, port))

  def listen(self, number = 5):
    self.socket.listen(number)
    self.running = True
    print("Waiting for connections...")

  def accept(self):
    return self.socket.accept()

  def broadcast(self , msg, prefix=""):
    for client in self.clients:
      client.send(bytes(prefix, "utf-8") + msg)

  def close_connections(self):
    self.broadcast("The server is shutting down")
    for socket in self.clients:
      socket.close()

  def shutdown(self):
    self.running = False
    self.close_connections()
    self.socket.close()
