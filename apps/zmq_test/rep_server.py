import zmq
from random import randrange
import time

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://127.0.0.1:5555")

while True:
    a = socket.recv()
    print('rec: {}'.format(a))
    time.sleep(5)
    socket.send_string("i receive a message: {}".format(a))
