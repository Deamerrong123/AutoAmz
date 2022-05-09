'''
REFERENCE CODE: https://pythonprogramming.net/server-chatroom-sockets-tutorial-python-3/
Modified by: Qizhao Rong
'''

import socket
import time
import GUI
import threading


HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 9998))
s.listen(5)

Win = threading.Thread(target = GUI.App)
Win.start()

while True:
    # now our endpoint knows about the OTHER endpoint.


    print("Waiting for Connection !!!")

    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")

    msg = "Welcome to the server!"
    msg = f"{len(msg):<{HEADERSIZE}}"+msg

    clientsocket.send(bytes(msg,"utf-8"))

    while True:
        time.sleep(3)
        msg = f"The time is {time.time()}"
        msg = f"{len(msg):<{HEADERSIZE}}"+msg

        print(msg)

        clientsocket.send(bytes(msg,"utf-8"))