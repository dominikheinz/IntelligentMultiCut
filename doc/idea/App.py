from tkinter import *
from sunditest import VideoCutter
import sys
class App:
    __sourcePaths = []
    __maxPaths=0
    __dynamic_widgets=[]

    def __init__(self, master,maxPaths):
        self.__maxPaths=maxPaths
        self.__sourcePaths=[None]*self.__maxPaths
        frame_1 = Frame(master)
        frame_1.grid()
        frame_1.configure(bg='#1D1D1D')
        frame_1.grid_rowconfigure(1, minsize=20)
        frame_1.grid_rowconfigure(9, minsize=20)
        frame_1.grid_columnconfigure(7, minsize=20)
        frame_1.grid_columnconfigure(0, minsize=20)
        frame_1.grid_rowconfigure(11, minsize=20)

        #Logo



        #Header

        w = Label(frame_1, text=" Welcome to Cam_Selector_v0.1",
                  fg='white', bg='#3299FD')
        w.configure(font=(None,10,'bold'))
        w.grid(row=0, column=0,sticky=W+E,columnspan=9)


        #Filepaths


        for i in range(0,self.__maxPaths):
            '''
            entry = Entry(frame_1)
            entry.grid(row=i + 2, column=1, columnspan=4, sticky=W
                      ,padx=2, pady=5)
            entry.configure(fg='#3299FD',bg='#1D1D1D',width=60,insertbackground='#3299FD')
            '''
            entry = Text(frame_1)
            entry.grid(row=i + 2, column=1, columnspan=4, sticky=W
                       , padx=2, pady=5)
            entry.configure(fg='#3299FD', bg='#1D1D1D',height=1, width=60, insertbackground='#3299FD',state='disabled')

            self.button2 = Button(frame_1,
                                  text="Browse", bg='#3299FD', fg='white',
                                  command=lambda i=i: self.browsepath(i))
            self.button2.configure(height=1, width=10, activeforeground='#3299FD',
                                   activebackground='#1D1D1D', bd=0)
            self.button2.grid(row=i+2, column=7)

            self.__dynamic_widgets.append(entry)
        #Buttons

        self.button1 = Button(frame_1,
                          text="Quit", bg='#E81123',fg='white',
                           command=frame_1.quit)
        self.button1.configure(height=1, width=10, activeforeground='white',
                              activebackground='#E81123',bd=0)
        self.button1.grid(row=10,column=1,pady=5,sticky=W)

        self.button3 = Button(frame_1,
                          text="Cut Videos",bg='#3299FD',fg='white',
                           command=self.cut_image_button)
        self.button3.configure(height=1, width=10,activeforeground='#3299FD',
                              activebackground='#1D1D1D',bd=0,state="disabled")


        self.button3.grid(row=10, column=6,padx=2,pady=5)

        self.button4 = Button(frame_1,
                             text="Calculate", bg='#3299FD', fg='white',
                             command=self.calculate)
        self.button4.configure(height=1, width=10, activeforeground='#3299FD',
                              activebackground='#1D1D1D', bd=0)

        self.button4.grid(row=10, column=7, padx=2)

        #Status Bar
        status= Label(frame_1,text='Status',bg='#1D1D1D',fg='white'
                      ,bd=1,relief=SUNKEN,anchor=W)
        status.grid(row=13,column=0,columnspan=9,sticky=W+E)

        #output
        self.output = Text(frame_1, width=80, height=8,relief=SUNKEN,bd=2,state='disabled',bg='#1D1D1D',fg='white',insertbackground='white')
        self.output.grid(row=12, column=0,columnspan=8,sticky=W)

        self.scrollbar = Scrollbar(frame_1, orient="vertical", command=self.output.yview,background='#1D1D1D')
        self.scrollbar.grid(row=12, column=8, sticky=E+N+S)

        self.output['yscrollcommand']=self.scrollbar.set
    def cut_image_button(self):

        out = "test_out"
        frame_jmps = [(0, 0 * 30), (2, 5 * 30), (1, 11 * 30), (0, 17 * 30)]
        fps = 30
        testSrc = app.get_paths()
        obj = VideoCutter((testSrc), out, frame_jmps, fps)
        obj.cut()

    def calculate(self):
        print("No function yet")

    def source_list_len(self):
        length=0
        for i in range (0,len(self.__sourcePaths)):
            if(self.__sourcePaths[i] is not None):
                length +=1
        return length
    def console_out(self,txt):
        self.output.config(state='normal')
        self.output.insert(INSERT,txt+'\n')
        self.output.config(state='disabled')
    def browsepath(self,index):
        from tkinter import filedialog
        Tk().withdraw()
        filename = filedialog.askopenfilename(filetypes = [("MPEG_4 files", "*.mp4"),
                                                           ("AVI files","*.avi")])
        if(filename!=""):

            self.__sourcePaths[index]=filename
            e=self.__dynamic_widgets[index]
            e.config(state='normal')
            e.delete(1.0,END)
            e.insert(INSERT,filename)
            e.config(state='disabled')
            self.console_out(filename+" was selected")

        if (self.source_list_len()==self.__maxPaths):
            self.button3.configure(state='normal')





    def get_paths(self):
        return self.__sourcePaths

root = Tk()
root.configure(background='#1D1D1D')
root.resizable(width=False,height=False)
app = App(root,6)
root.mainloop()