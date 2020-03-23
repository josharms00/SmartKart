import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
import socket
import numpy as np
import pickle
import argparse
import time
mnist = tf.keras.datasets.mnist

buttons = [
	"P1 A",
	"P1 A Down",
	"P1 A Left",
	"P1 A Right",
	"P1 A Up",
	"P1 B",
	"P1 C Down",
	"P1 C Left",
	"P1 C Right",
	"P1 C Up",
	"P1 DPad D",
	"P1 DPad L",
	"P1 DPad R",
	"P1 DPad U",
	"P1 L",
	"P1 R",
	"P1 Z"
]

hot_encodings = np.array([
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
])

def one_hot_encode(index_list):
	hot_stuff = np.zeros((17,))
	for index in index_list:
		hot_stuff += hot_encodings[index]

	return hot_stuff


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
			Y = np.array(data[1].split("#"))
			Y_indices = []

			for button in Y:
				Y_indices.append(buttons.index(button))

			one_hots = one_hot_encode(Y_indices)

			train.append(X.astype(np.float))
			labels.append(one_hots)

		line = file.readline().strip("\n")

	tp = open('training_data/train.pickle', 'wb')
	pickle.dump(train, tp)

	lp = open('training_data/labels.pickle', 'wb')
	pickle.dump(labels, lp)

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

	return clientsocket

def determine_action(clientsocket):
	while True:
		try:
			state = clientsocket.recv(240)
			packet = state.decode().strip("\n")
	
			data = packet.split(" ")

			selected_buttons = predict(data) + "\n"

			clientsocket.send(selected_buttons.encode())
		except KeyboardInterrupt:
			print("Exception occurred. Closing connection.")
			print(traceback.print_exc())
			clientsocket.send(b"close")
			clientsocket.close()
			break

def get_model():
	model = Sequential()

	model.add(LSTM(20, input_shape=(super_t.shape[1:]), activation='relu', return_sequences=True))
	model.add(Dropout(0.2))

	model.add(LSTM(20, activation='relu'))
	model.add(Dropout(0.2))

	model.add(Dense(17, activation="sigmoid"))

	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

	return model

def predict(data):
	model = tf.keras.models.load_model('1583692534.896509.h')

	inputs = np.array(data).astype(np.float)

	choices = model.predict(inputs.reshape(1, 6, 1))

	selected_buttons = ""

	for i in range(len(choices[0])):
		if choices[0][i] > 0.5:
			selected_buttons += str(i + 1) + " "

	return selected_buttons

def train():
	train_data = pickle.load(open('training_data/train.pickle', 'br'))

	train_labels = pickle.load(open('training_data/labels.pickle', 'br'))

	# data must be put into an numpy array
	t = np.array(train_data)

	# labels must be put into an numpy array
	l = np.array(train_labels)

	super_t = t.reshape(t.shape[0], t.shape[1], 1)

	model = get_model()

	model.fit(super_t, l, epochs=1)

	model.save(str(time.time()) + ".h")

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
		clientsocket = start_server()
		determine_action(clientsocket)

	elif args.train:
		if not args.pickled:
			prep_data()
		train()

if __name__ == "__main__":
	main()
