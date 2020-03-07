import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
import socket
import numpy as np
import pickle
import argparse
import time

clientsocket = []

def prep_data():
	file = open("lua/data.txt", "r")

	i = 0
	data = []

	train = []
	labels = []

	line = file.readline().strip("\n")

	while line:		
		data = line.split("#b#")

		if len(data) > 1:
			if data[1] == '': 
				line = file.readline().strip("\n")
				continue

			X = np.array(data[0].split("#"))
			Y = data[1].split("#")

			train.append(X.astype(np.float))
			labels.append(Y)

		line = file.readline().strip("\n")

	tp = open('training_data/train.pickle', 'wb')
	pickle.dump(train, tp)

	lp = open('training_data/labels.pickle', 'wb')
	pickle.dump(labels, lp)

def train():
	train_data = pickle.load(open('training_data/train.pickle', 'br'))

	train_labels = pickle.load(open('training_data/labels.pickle', 'br'))

	model = initialize_model()

	# data must be put into an numpy array
    train_data = np.array(train_labels)
	
	# labels must be put into an numpy array
    train_labels = np.array(train_labels)

	model.fit(train_data, train_labels, epochs=1)

	model.save()
	

def start_server():
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

def initialize_model():
	model = Sequential()

	model.add(LSTM(10, input_shape=(6,), return_sequences=True))

	model.add(LSTM(20))
	model.add(LSTM(20))

	model.add(Dense(17, activation="sigmoid"))

	model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])

	return model

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('-t', '--train',
            action="store_true", dest="train",
            help="train model")

	parser.add_argument('-r', '--run',
            action="store_true", dest="run",
            help="run model in the emualtor")

	parser.add_argument('-p', '--pickled',
		action="store_true", dest="pickled",
		help="data to train has already been preped and pickled")

	args = parser.parse_args()

	if args.run: 
		start_server()
		determine_action()

	elif args.train:
		if not args.pickled:
			prep_data()
		train()

if __name__ == "__main__":
	main()
