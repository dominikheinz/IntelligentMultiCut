from src.classes.core.Base import Base
from src.classes.view.GUI import GUI

from multiprocessing import Process, Queue, JoinableQueue
from src.classes.controllers.ProgressController import ProgressController
from src.classes.controllers.OpenPoseController import OpenPoseController
from src.classes.controllers.CleanController import CleanerController

class App(Base):

    def __init__(self):
        self.__gui = GUI()
        self.__gui.root.mainloop()
