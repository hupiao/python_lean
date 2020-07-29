import sys
import zmq

#  Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from weather server...")
socket.connect("tcp://localhost:5556")

# Subscribe to zipcode, default is NYC, 10001
zip_filter = sys.argv[1] if len(sys.argv) > 1 else "10002"

# 此处设置过滤条件，只有以 zip_filter 开头的消息才会被接收
socket.setsockopt_string(zmq.SUBSCRIBE, '')


# Process 5 updates
total_temp = 0
for update_nbr in range(5):
    string = socket.recv()
    print(string)
import time
time.sleep(8)
socket.connect("tcp://localhost:5557")
while True:
    print(socket.recv())
