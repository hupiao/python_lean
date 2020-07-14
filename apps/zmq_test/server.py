#-*-coding:utf-8-*-
import zmq
import sys
import time
import random
context = zmq.Context()
socket = context.socket(zmq.REP)
# socket.setsockopt(zmq.RCVTIMEO, 5)
socket.bind("tcp://*:5555")
while True:
    try:
        print("wait for client ...")
        message = socket.recv()
        print("message from client:", message.decode('utf-8'))
        i = random.randint(0,2)
        print(i)
        time.sleep(i)
        socket.send(message)

    except Exception as e:
        print('异常:', e)
        sys.exit()
