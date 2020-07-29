import zmq
from random import randrange

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")
import  time
while True:
    time.sleep(2)
    socket.send_string("xixixixix")
