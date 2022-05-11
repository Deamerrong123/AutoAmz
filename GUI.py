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
        self.clients = []

        # bool obj
        self.Gui_done = False
        self.running = True
        self.recieve_mode = False

        # thread for handeling GUI
        self.Gui_thread = threading.Thread(target = self.Gui,args = ())
        self.Gui_thread.start()


        # Once GUI window working, we can conncet to the ONLY Client
        self.Client, _ = self.conncet()

        # Once they host the connection, start a thread for handling
        # reciving message.
        self.Recieving = threading.Thread(target = self.recieve_message,args=(self.Client,))
        self.Recieving.start()

    def conncet(self):
        try:
            # we only need to connect to one device
            clientsocket, address = self.server.accept()
            self.clients.append(clientsocket)
            msg = "Welcome to the server!"
            msg = f"{len(msg):<{HEADERSIZE}}"+msg
            clientsocket.send(bytes(msg,"utf-8"))

        except Exception as e:
            # self.server.close()
            # # self.root.destroy()
            # sys.exit()
            print(str(e))

        return clientsocket , address

    def Gui(self):

        self.root = Tk() # root window
        self.root.geometry("1040x600")

        # create first frame, and attach on the the top root win
        self._top = ttk.Frame(self.root,padding = '5 5 5 10')
        self._top.grid(row=0,column=0)

        # create a text Entry on the top and stand on the middle
        self._code = StringVar()
        self._code.set("Enter code here !")
        self._entry = ttk.Entry(self._top,textvariable = self._code,width = 50,
                                font=('calibre',20,'normal'),justify=tkinter.CENTER)
        self._entry.grid(row=0,column=0)
        # create a button
        self._button = ttk.Button(self._top,text =
                                  "Submit",command = self.submit).grid(row=0,column=1,padx=10)
        

        # create bottom framework
        self._down = ttk.Frame(self.root)
        self._down.grid(row = 1, column=0)

        l_win = PanedWindow(self._down,bg = 'light pink',borderwidth = 10)
        r_win = PanedWindow(self._down, bg = 'light green',borderwidth = 10)
        l_win.pack(side = tkinter.LEFT)
        r_win.pack(side = tkinter.RIGHT)

        # create two Canvas win, where for displaying recieved imagess
        self._Can1 = Canvas(l_win,width = 500,height = 500)
        self._Can1.configure(bg = 'white')
        self._Can1.pack()
        
        self._Can2 = Canvas(r_win,width = 500,height=500)
        self._Can2.configure(bg = 'white')
        self._Can2.pack()


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

        except:
            print("ERROR -> handle_message")
            exit(1)

    def recieve_message(self,CliendSock):
            while self.running:
                try:
                    msg = CliendSock.recv(1024)
                    print(msg.decode('utf-8\n\n'))

                    if msg == b'%DONE%':
                        print("Start reciving image... \n")
                        file_name = CliendSock.recv(1024)
                        file_name = file_name.decode('utf-8')

                        if file_name != 'error':

                            file_stream = io.BytesIO()
                            recv_data = CliendSock.recv(BUFFER_SIZE)

                            while recv_data:
                                file_stream.write(recv_data)
                                recv_data = CliendSock.recv(BUFFER_SIZE)

                                if recv_data == b'%IMAGE_COMPLETE%':
                                    break # exit the 'inner' while loop

                            img = Image.open(file_stream)
                            file_name = os.path.join(today_path,file_name)
                            img.save(file_name, format ='PNG')
                        print("Image Complete\n")

                except Exception as e:
                    print("ERROR -> recieve_message")
                    print(f'{str(e)}')

            return True

    def submit(self):
        '''
        1. send out the CODE from the server side
        2. wait for respondes from the cliend side.
        3. once the image recieve, displayed it right the way
        '''
        # get the CODE
        CODE = self._code.get()
        if len(CODE) > 4:

            if self.handle_message(self.Client,CODE):
                # time.sleep(5)
                # once handle_message is COMPLETE, the desired png should be appear.
                # for file_name in os.listdir(today_path):
                #     if CODE in file_name:
                #         self.updata_image(file_name)
                pass



    def updata_image(self,file_name):
        '''
        1. make sure the dir is not empty.
        2. pick the correct image from the dir and paste it on the right side
        '''
        
        if "successfully" in file_name:
            file_name = os.path.join(today_path,file_name)

            #Load an image in the script
            img= Image.open(file_name)

            #Resize the Image using resize method
            resized_image= img.resize((500,500), Image.ANTIALIAS)
            new_image= ImageTk.PhotoImage(resized_image)

            ## put it up to the _Can2
            self._Can2.create_image(0,0, anchor=tkinter.NW, image = new_image)
            self._Can2.image = new_image

        else:
            file_name = os.path.join(today_path,file_name)
            #Load an image in the script
            img= Image.open(file_name)

            #Resize the Image using resize method
            resized_image= img.resize((500,500), Image.ANTIALIAS)
            new_image= ImageTk.PhotoImage(resized_image)

            ## put it up to the _Can2
            self._Can1.create_image(0,0, anchor=tkinter.NW, image = new_image)
            self._Can1.image = new_image


    def clear(self):
        pass

if __name__ == '__main__':
    application = App()
