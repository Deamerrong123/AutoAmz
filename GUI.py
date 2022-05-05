from tkinter import ttk,Tk,StringVar,Canvas,PanedWindow
from tkinter import BOTH as tkboth
import tkinter
from PIL import Image , ImageTk
import os


class App(object):

    def __init__(self):
        root = Tk() # root window
        root.geometry("1040x600")

        # create first frame, and attach on the the top root win
        self._top = ttk.Frame(root,padding = '5 5 5 10')
        self._top.grid(row=0,column=0)

        # create a text Entry on the top and stand on the middle
        self._code = StringVar()
        self._code.set("Enter code here !")
        self._entry = ttk.Entry(self._top,textvariable = self._code,width = 50,
                                font=('calibre',20,'normal'))
        self._entry.grid(row=0,column=0)
        # create a button
        self._button = ttk.Button(self._top,text =
                                  "Click").grid(row=0,column=1,padx=10)

        # create bottom framework
        self._down = ttk.Frame(root)
        self._down.grid(row = 1, column=0)

        l_win = PanedWindow(self._down,bg = 'light pink',borderwidth = 10)
        r_win = PanedWindow(self._down, bg = 'light green',borderwidth = 10)
        l_win.pack(side = tkinter.LEFT)
        r_win.pack(side = tkinter.RIGHT)

        # create two Canvas win, where for displaying recieved imagess
        self._Can1 = Canvas(l_win,width = 500,height = 500)
        self._Can1.configure(bg = 'white')
        self._Can1.pack()
        # self._Can1.grid(row=0,column=0,padx = 10)
        
        self._Can2 = Canvas(r_win,width = 500,height=500)
        self._Can2.configure(bg = 'white')
        self._Can2.pack()        
        # self._Can2.grid(row=0,column=1,padx = 10)

        # Entry on the top

        root.mainloop()


    def submit(self):
        '''
        1. send out the CODE from the server side
        2. wait for respondes from the cliend side.
        3. once the image recieve, displayed it right the way
        '''
        # get the CODE
        CODE = self._code.get()
        if not CODE:

            #send_message(CODE)
            self.updata_image()



    def updata_image(self):
        '''
        1. make sure the dir is not empty.
        2. pick the correct image from the dir and paste it on the right side
        '''
        pass



    def clear(self):
        pass
    

    


if __name__ == '__main__':

    application = App()
