import zmq
import random

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:7002")
socket.send_pyobj(random.randint(0, 10))
message = socket.recv()
print ("Received reply ", "[", message, "]")
