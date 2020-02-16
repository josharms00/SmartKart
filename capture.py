import tensorflow as tf
from tensorflow.keras.models import Sequential
import socket

# start server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 120
server.bind((socket.gethostname(), port))
print("Hostname: %s Port: %d" % (socket.gethostname(), port))
server.listen(1)

# wait for connection from the emulator script
print("Listening for connection on port %d..." % (port,))
(clientsocket, address) = server.accept()
print("Received client at %s:%d" % (address, port))

def determine_action():
	buttons = clientsocket.recv(1)
	clientsocket.send("1".encode())

def initialize_model(nhiddenlayers):
	model = Sequential()

def main():
	while True:
		determine_action()

if __name__ == "__main__":
	main()
