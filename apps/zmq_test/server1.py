#!/usr/bin/pyth
# #-*-coding:utf-8-*-
import time
import zmq
import msgpack

context = zmq.Context()
sender = context.socket(zmq.PUSH)
sender.sndhwm = 10
sender.setsockopt(zmq.IPV6, 1)
sender.bind("tcp://127.0.0.1:5555")

while True:
    msg = sender.send(msgpack.dumps('2'))
    time.sleep(4)

