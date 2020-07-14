# -*-coding:utf-8-*-
import zmq
import sys
import logging
# context = zmq.Context()
# print("Connecting to server...")
# socket = context.socket(zmq.REQ)
# socket.setsockopt(zmq.RCVTIMEO, 1000)
# socket.connect("tcp://localhost:5555")
# socket.setsockopt
# socket.setsockopt(zmq.RCVTIMEO, 1)
# while True:
#     try:
#         input1 = input("请输入内容：").strip()
#         if input1 == 'b':
#             sys.exit()
#         socket.send(input1.encode('utf-8'), copy=False)
#
#         message = socket.recv()
#         print("Received reply: ", message.decode('utf-8'))
#     except Exception as err:
#         print(err)


class Sender(object):
    context = None

    def __init__(self, queue_name, context=None, send_type=zmq.PUSH):
        if context is None:
            self.context = zmq.Context()
        else:
            self.context = context
        self.queue_name = queue_name
        self.send_type = send_type
        self._connect()

    def _connect(self):
        self.sender = self.context.socket(self.send_type)
        self.sender.sndhwm = 10000
        self.sender.linger = -1
        self.sender.setsockopt(zmq.RCVTIMEO, 1000)  # 设置recv超时时间 3s
        self.sender.connect(self.queue_name)

    def send_data(self, data):
        try:
            self.sender.send(data, zmq.NOBLOCK, copy=False)
        except Exception as err:
            return False, err
        return True, ""

    def send_data_by_req(self, data):
        try:
            q = self.sender.send(data, copy=False)
            print(q)
            return self.sender.recv()
        except Exception as err:
            # logging.exception(err)
            print(type(err))
            self._connect()
        return {}


sender = Sender(queue_name="tcp://localhost:5555", send_type=zmq.REQ)
while True:
    input1 = input("请输入内容：").strip()
    if input1 == 'b':
        sys.exit()
    print(sender.send_data_by_req(input1.encode('utf-8')))
    print('================')
