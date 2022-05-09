'''
REFERENCE CODE: https://pythonprogramming.net/server-chatroom-sockets-tutorial-python-3/
Modified by: Qizhao Rong
'''

import socket
import select
import errno

## CONSTANT
HEADER_LENGTH = 10
BUFFER_SIZE = 4096
IP = socket.gethostname()
PORT = 9998

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

''''''
def uploading_PNG(client,code):
    pass



''''''

first_conn = client_socket.recv(1024).decode('utf-8')
if first_conn:
    print(first_conn)

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
                print(CODE.decode('utf-8'))
                # then working on AutoAmz.
                #
                # once it is done.
                client_socket.send(b'DONE')
                uploading_PNG(client_socket,CODE)
                client_socket.send(b'IMAGE_COMPLETE')



    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: '.format(str(e)))
        sys.exit()