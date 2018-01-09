from tkinter import *
from tkinter import filedialog


class GUI:

    __dark = '#1D1D1D'
    __blue = '#3299FD'
    __sourcePaths = []
    __buttonLabels=["Browse","Cut","Finish"]
    __menuCounter=0
    __functions=[]
    __cancel_browse=False

    def __init__(self,master):

        self.frame_1 = Frame(master, bg=self.__dark)
        self.frame_1.grid(row=0,column=0)

        self.__functions.append(self.browsepath)
        self.__functions.append(self.sunditest)
        self.__functions.append(self.frame_1.quit)

        self.label=Label(self.frame_1,bg=self.__dark,text="Welcome to MagiCam",font=(None,15,'bold'),fg='white')
        self.label.grid(row=1,column=5,padx=20,pady=20)
        self.button1 = Button(self.frame_1, text='Let\'s Go!', bg=self.__blue, fg='white', activeforeground='#3299FD',
                              activebackground='#1D1D1D', bd=0, font=(None, 12, 'bold'), width=40, height=3,
                              command=lambda: self.next_page(self.button1, self.frame_1))

        self.button1.grid(row=10, column=5)
        self.frame_1.rowconfigure(9,minsize=20)
        self.event_handler(self.button1, "hover", "cursor", "hand2")


    def next_page(self, widget, master):

            self.destroy_me(widget)
            if (self.__menuCounter < len(self.__functions)):
                self.new_button(master, self.__functions[self.__menuCounter])


    def new_button(self,master,function):
                button=Button(master, text=self.__buttonLabels[self.__menuCounter], bg=self.__blue, fg='white', activeforeground='#3299FD',
                              activebackground='#1D1D1D', bd=0, font=(None, 12, 'bold'),width=40,height=3,
                              command=lambda : [function(),self.next_page(button, master)])
                button.grid(row=10, column=5)
                self.event_handler(button, "hover", "cursor", "hand2")
                self.__menuCounter+=1
                '''if (function == self.sunditest):
                    self.__menuCounter-=1
                    button = Button(master, text=self.__buttonLabels[self.__menuCounter], bg=self.__blue, fg='white',
                                    activeforeground='#3299FD',
                                    activebackground='#1D1D1D', bd=0, font=(None, 12, 'bold'), width=40, height=3,
                                    command=lambda: function())
                    button.grid(row=10, column=4)
                    self.event_handler(button, "hover", "cursor", "hand2")
                '''



    def destroy_me(self,widget):
        widget.grid_forget()


    def event_handler(self,widget,event,mode,value):

        if (event == "hover"):
            if(mode=="text"):
                widget.bind("<Enter>", lambda x, txt=value: self.status.config(text=txt))
                widget.bind("<Leave>", lambda x, txt='': self.status.config(text=txt))
            if(mode=="cursor"):
                widget.bind("<Enter>", lambda x, cursor=value: widget.config(cursor=cursor))
                widget.bind("<Leave>", lambda x, cursor=None: widget.config(cursor=cursor))


    def sunditest(self):
       print ("Test")


    def browsepath(self):

        Tk().withdraw()
        filenames = filedialog.askopenfilenames(filetypes=[("MPEG_4 files", "*.mp4"),
                                                         ("AVI files", "*.avi")])
        if (len(filenames) != 0):
            self.__sourcePaths=filenames
            print(self.__sourcePaths)
            print(len(self.__sourcePaths))
            for i in range (0,len(self.__sourcePaths)) :
                self.input=Text(self.frame_1, fg='#3299FD',font=(None, 10, 'bold'), bg='#1D1D1D', height=1
                                 , insertbackground='#3299FD',width=32)
                self.input.grid(row=i+2, column=5,pady=3)
                self.input.config(state='normal')
                self.input.delete(1.0, END)
                vid_name=self.__sourcePaths[i]
                index=vid_name.rfind('/')+1
                self.input.insert(INSERT, vid_name[index:])
                self.input.config(state='disabled')

        else:
            self.__menuCounter-=1                           #Browse didnt get a filename
            #self.console_out(filename + " was selected")


root = Tk()
root.configure(background='#1D1D1D')
root.resizable(width=False,height=False)
app = GUI(root)
root.mainloop()