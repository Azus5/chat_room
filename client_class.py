import socket

class Client:
  def __init__(self, host, port = 12397, buffer_size = 1024):
    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.buffer_size = buffer_size
    self.host = host
    self.port = port

  def connect(self):
    self.socket.connect((self.host, self.port))

  def close(self):
    self.socket.close()

  def send(self, string):
    self.socket.send(bytes(string, "utf-8"))

  def recv(self):
    return self.socket.recv(self.buffer_size).decode("utf-8")