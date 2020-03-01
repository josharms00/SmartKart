import tensorflow as tf
from tensorflow.keras.models import Sequential
import socket

st = "1 2 \n"

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
	while True:
		try:
			buttons = clientsocket.recv(20)
			if buttons.decode() == "P1 A":
				print("nice")
			clientsocket.send(st.encode())
		except KeyboardInterrupt:
			print("Exception occurred. Closing connection.")
			print(traceback.print_exc())
			clientsocket.send(b"close")
			clientsocket.close()
			break

def initialize_model(nhiddenlayers):
	model = Sequential()

def main():
	determine_action()

if __name__ == "__main__":
	main()
