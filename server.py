from server_class import ServerSocket
from threading import Thread

def accept_connections(server_socket):
  while True:
    try:
      client, client_address = server_socket.accept()
      print("%s: Entered the chat!" % client_address[0])
      client.send(bytes("Type your message, and press enter (quit! to exit), ", "utf-8"))
      server_socket.addresses[client] = client_address

      Thread(target=handle_client,  args=(client, server_socket)).start()
    except KeyboardInterrupt:
      server_socket.shutdown()
      break

def handle_client(client, server_socket):
  BUFFER_SIZE = 1024
  name = client.recv(BUFFER_SIZE).decode("utf-8")
  server_socket.broadcast(bytes("%s entered the chat" % name, "utf-8"))
  server_socket.clients[client] = name

  while server_socket.running:
    try:
      msg = client.recv(BUFFER_SIZE)
      if (msg != bytes("quit!", "utf-8")):
        server_socket.broadcast(msg, name+": ")
      else:
        client.send(bytes("quit!", "utf-8"))
        client.close()
        del server_socket.clients[client]
        server_socket.broadcast(bytes("%s exit the chat" % name, "utf-8"))
        break
    except KeyboardInterrupt:
      server_socket.shutdown()
      break

if __name__ == "__main__":
  HOST = '192.168.0.112'
  PORT = 12397
  server_socket = ServerSocket(HOST, PORT)
  server_socket.listen()

  ACCEPT_THREAD = Thread(target=accept_connections, args=[server_socket])
  ACCEPT_THREAD.start()
  ACCEPT_THREAD.join()