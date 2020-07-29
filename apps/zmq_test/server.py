import zmq
from random import randrange

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5557")

import time
while True:
    time.sleep(1)
    socket.send_string("hahahahahah")
