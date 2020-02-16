import tensorflow as tf
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 120
server.bind((socket.gethostname(), port))
print("Hostname: %s Port: %d" % (socket.gethostname(), port))
server.listen(1)

while True:
	print("Listening for connection on port %d..." % (port,))
	(clientsocket, address) = server.accept()
	print("Received client at %s:%d" % (address, port))
	buttons = clientsocket.recv(1)
	print(buttons)