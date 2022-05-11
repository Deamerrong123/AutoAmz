'''
REFERENCE CODE: https://pythonprogramming.net/server-chatroom-sockets-tutorial-python-3/
Modified by: Qizhao Rong
'''

import socket
import errno
from datetime import datetime
import os
import sys

## CONSTANT
HEADER_LENGTH = 10
BUFFER_SIZE = 4096

# Once the server hosting using ngrok, we need the
# ip address and the port. 
IP = str(input("Enter the TCP IP address: "))
PORT = int(input("Enter the PORT number: "))


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
##client_socket.setblocking(False)

# Create the working dir for TODAY CLIENT
TODAY = datetime.today()
today_path = f'Client_{TODAY.month}_{TODAY.day}'
if not os.path.isdir(today_path):
    os.mkdir(today_path)

''' def functions on below;
'''

def uploading_PNG(client,code):
    '''
    1. locate the file_name contain the code
    2. send the file_name first
    3. send the file(.png).
    '''
    for file_name in os.listdir(today_path):
        if code in file_name:
            file = os.path.join(today_path,file_name)
            print(file_name)
            client.send(bytes(file_name,'utf-8')) # send the file_name first
            # then packing the file into bytes and sent.
            with open(file,'rb') as f:
                file_data = f.read(BUFFER_SIZE)

                while file_data:
                    client.send(file_data)
                    file_data = f.read(BUFFER_SIZE)
            # once the image been successully transmited, we tell the 
            # server it is done.
            client_socket.send(b'%IMAGE_COMPLETE%')

            return True

        # if we cannot locate the file, tell the server and stop sending.
        client.send(bytes('error','utf-8'))
        return False
''''''

first_conn = client_socket.recv(1024)
if first_conn:
    print(first_conn.decode('utf-8'))

while True:

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            ## handle message(CODE) recieve from server
            CODE = client_socket.recv(1024)
            if not CODE:
                continue
            else:
                # once we have the CODE.
                CODE = CODE.decode('utf-8')
                print(CODE)
                # then working on AutoAmz.
                # sleep(3)
                # once it is done.
                client_socket.send(b'%DONE%')
                uploading_PNG(client_socket,CODE)


    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error : {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue

    # except Exception as e:
    #     # Any other exception - something happened, exit
    #     print('Reading error: '.format(str(e)))
    #     sys.exit()
