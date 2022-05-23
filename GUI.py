## libray for GUI
from tkinter import ttk,Tk,StringVar,Canvas,PanedWindow
from tkinter import BOTH as tkboth
import tkinter
from PIL import Image , ImageTk
import os
from datetime import datetime

## library for connection
import socket
import threading
import sys
import io

## CONSTANT
TODAY = datetime.today()
today_path = f'server_{TODAY.month}_{TODAY.day}'
HEADERSIZE = 10
BUFFER_SIZE = 4096


if not os.path.isdir(today_path):
    os.mkdir(today_path)


class App(object):

    def __init__(self):
        ## handel for the server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(("localhost", 9998)) # connect to localhost
        self.server.listen()
        self.Clients = []

        # bool obj
        self.Gui_done = False
        self.running = True
        self.Gui()



    def conncet(self):
        print("We are seeking for connection with THIS Server")
        try:
            # we only need to connect to one device
            clientsocket, address = self.server.accept()
            self.Clients.append(clientsocket)
            print(f'We have connect to {address}.')

            msg = "Welcome to the server!"
            msg = f"{len(msg):<{HEADERSIZE}}"+msg
            clientsocket.send(bytes(msg,"utf-8"))

        except Exception as e:
            # self.server.close()
            # # self.root.destroy()
            # sys.exit()
            print(str(e))


    def Gui(self):

        self.root = Tk() # root window
        self.root.geometry("1040x610")

        # create first frame, and attach on the the top root win
        self._top = ttk.Frame(self.root,padding = '5 5 5 10')
        self._top.grid(row=0,column=0)

        # create a text Entry on the top and stand on the middle
        self._code = StringVar()
        self._code.set("Enter code here !")
        self.ref_btn = ttk.Button(self._top,text = "Connect",command = self.conncet).grid(row = 0,column= 0,padx = 10)
        self._entry = ttk.Entry(self._top,textvariable = self._code,width = 50,
                                font=('calibre',20,'normal'),justify=tkinter.CENTER)
        self._entry.grid(row=0,column=1)
        # create a button
        self._button = ttk.Button(self._top,text =
                                  "Submit",command = self.submit).grid(row=0,column=2,padx=10)

        # create bottom framework
        self._down = ttk.Frame(self.root)
        self._down.grid(row = 1, column=0)
        self._Can1 = Canvas(self._down,width = 1000,height = 500)
        self._Can1.configure(bg = 'white',borderwidth = 20)
        self._Can1.pack()

        self.Gui_done = True
        self.root.protocol("WM_DELETE_WINDOW",self.stop)

        self.root.mainloop()

    def stop(self):
        self.running = False
        self.root.destroy()
        self.server.close()
        exit(0)


    def handle_message(self,CliendSock,_text):
        # conver string into bytes
        msg = bytes(_text,'utf-8')
        # be careful about disconnection
        try:
            CliendSock.send(msg)
            self.running = True
            # Once they host the connection, start a thread for handling
            # reciving message.
            self.Recieving = threading.Thread(target = self.recieve_message,args=(CliendSock,))
            self.Recieving.start()
            self.Recieving.join()

        except:
            print("ERROR -> handle_message()")
            exit(1)

    def recieve_message(self,CliendSock):
            while self.running:
                try:
                
                    msg = CliendSock.recv(1024)
                    print(f'{msg}')

                    if msg == b'%DONE%':
                        print("Start reciving image... \n")
                        fname = CliendSock.recv(1024) ## here is the file name
                        print(fname)
                        

                        if fname == b'error': 
                            print("This section is closed.")
                            raise ValueError

                        else:

                            file_stream = io.BytesIO()
                            recv_data = CliendSock.recv(BUFFER_SIZE)

                            while recv_data:
                                file_stream.write(recv_data)
                                recv_data = CliendSock.recv(BUFFER_SIZE)

                                if recv_data == b'%IMAGE_COMPLETE%':
                                    break # exit the 'inner' while loop
                            file_name = fname.decode('utf-8') ## decode the b'' into string
                            # print(file_name)
                            img = Image.open(file_stream)
                            file_name = os.path.join(today_path,file_name)
                            img.save(file_name, format ='PNG')

                            print("Image Complete\n")
                            raise ValueError

                except ValueError:
                    print("Want to terminate thread.")
                    self.running = False
                except Exception as ec:
                    print("ERROR -> recieve_message()")
                    print(str(ec))
                
                finally:   
                    self.running = False # kill this thread (reciving)

    def submit(self):
        '''
        1. send out the CODE from the server side
        2. wait for respondes from the cliend side.
        3. once the image recieve, displayed it right the way
        '''
        # get the CODE
        CODE = self._code.get()
        if len(CODE) > 4:

            self._Can1.delete("all")
            Client = self.Clients[-1]
            self.handle_message(Client,CODE)
            # once handle_message is COMPLETE, the desired png should be appear.

            print("something something...")

            for file_name in os.listdir(today_path):
                if CODE in file_name:
                    self.updata_image(file_name)

    def updata_image(self,file_name):
        '''
        1. make sure the dir is not empty.
        2. pick the correct image from the dir and paste it on the right side
        '''
        file_name = os.path.join(today_path,file_name)
        #Load an image in the script
        img= Image.open(file_name)

        print("almost there...")

        #Resize the Image using resize method
        resized_image= img.resize((1000,500), Image.ANTIALIAS)
        new_image= ImageTk.PhotoImage(resized_image)

        ## put it up to the _Can1
        self._Can1.create_image(0,0, anchor=tkinter.NW, image = new_image)
        self._Can1.image = new_image


    def clear(self):
        pass

if __name__ == '__main__':
    application = App()
