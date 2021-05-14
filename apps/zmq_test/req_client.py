import zmq
import random

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://127.0.0.1:5555")

while True:
    msg = random.randint(0, 100000)
    socket.send_string(str(msg))
    print(socket.recv())
    print('==========================')
