import tensorflow as tf
from tensorflow.keras.models import Sequential
import socket
import numpy as np
import pickle

def prep_data():
	file = open("lua/data.txt", "r")

	data = []

	train = []
	labels = []

	line = file.readline()
	data.append(line)

	while line:
		if "|" in line:
			line = file.readline()
			sp = line.split("|")
			data[i] += sp[0]
			data.append(sp[1])

			i += 1
		else:
			data[i] += line

	for d in data:
		butt = s.split("#b#")
		X = np.array(butt[0].split("#"))
		Y = butt[1].split("#")

		train.append(X.astype(np.float))
		lables.append(Y)

	tp = open('training_data/train.pickle', 'wb')
	pickle.dump(X, tp)

	lp = open('training_data/labels.pickle', 'wb')
	pickle.dump(Y, lp)

def train():
	print("training")

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
			buttons = clientsocket.recv(240)
			packet = buttons.decode()
			data = packet.split(" ", 0)

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
	parser.add_argument('-t', '--train',
            action="store_true", dest="train",
            help="train model")

	parser.add_argument('-r', '--run',
            action="store_true", dest="run",
            help="run model in the emualtor")

	args = parser.parse_args()

	if args.run: 
		determine_action()

	elif args.train:
		prep_data()
		train()

if __name__ == "__main__":
	main()
