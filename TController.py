import time
import zmq
import multiprocessing
import atexit

server_ports = {"twitter"   : 7000,
                "facebook"  : 7001,
                "twitch"    : 7002,
                "other"     : 7003}

def server(currentValues,name):
    port = server_ports[name]
    with zmq.Context() as context:
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:%s" % port)
        print(name + " %s running server on port: %d" % (name, port))
        while True:
            # Wait for next request from client
            message = socket.recv_pyobj()
            print("Received notification from %s: %s" % (name, message))
            currentValues[name] = message
            socket.send_string("Message Recieved %s" % port)

if __name__ == '__main__':
    mgr = multiprocessing.Manager()
    currentValues = mgr.dict()
    currentValues.update({  'twitter'       : 0, 
                            'facebook'      : 0, 
                            'fb_comments'   : 0,
                            'twitch'        : 0})

    server_list = [ multiprocessing.Process(target=server, 
                            args=(currentValues, names)) for names in list(server_ports.keys())]
    for j in server_list:
        j.daemon = True
        j.start()

    while True:
        print(currentValues)
        time.sleep(1)




