import time
from src.classes.controllers.OpenPoseController import OpenPoseController
from src.classes.core.Base import Base
from src.classes.controllers.MetaDataController import MetaDataController
from src.classes.controllers.AlgorithmController import AlgorithmController
from src.classes.controllers.CutterController import CutterController
from src.classes.controllers.ProgressController import ProgressController
from threading import *
from src.classes.controllers.SyncController import SyncController
from src.classes.controllers.CleanController import CleanerController
import time
from tkinter import filedialog
import shutil
import pprint


class View(Base):

    __progress_thread = 0
    filepaths = []

    def __init__(self):
        # erstellt leeren Container für den Hauptthread des Prozesses
        self.__running_thread = False
        self.cleaner = CleanerController()
        self.__openPose = False


    def process(self):
        print("cleaning old files ...")
        self.cleaner.clean_workspace()
        self.__running_thread = Thread(target=self.thread)
        self.__running_thread.start()

    def thread(self):
        self.processing = True

        self.console_out("[Status]: Start processing...")

        if self.config.get("auto_sync"):
            sync = SyncController(self.filepaths)
            tupel = sync.audio_analyse()
            sync = CutterController(self.filepaths, tupel, 29)
            self.filepaths = sync.clap_sync("../import/video/")

        self.set_progress(self.get_progress() + 2)
        time.sleep(1)
        self.set_progress(self.get_progress() + 3)

        self.progress = ProgressController(self, self.filepaths)
        self.__progress_thread = Thread(target=self.progress.calculate_progress)
        self.__progress_thread.start()

        if not self.config.get("debug"):
            self.__openPose = OpenPoseController()

            self.console_out("[Status]: Start pose analysis...")

            # startet OpenPose
            self.__openPose.process(self.filepaths)

            self.console_out("[Status]: Pose analysis is complete")

        else:
            self.console_out("[Debug]: Skip pose estimation")

        self.console_out("Processing is complete")

        # Berechnet die zu schneidenden Frames
        self.metadata_controller = MetaDataController()

        self.set_progress(self.get_progress() + 5)

        # Algo-ID Explanation :
        # 0 : Pose Algorithm
        # 1 : Distance Algorithm
        # 2 : Multiperson Algorithm
        show_graph = self.config.get("show_algo_graphs")
        algo_id = self.config.get("algorithm")

        ctrl = AlgorithmController(self.metadata_controller)
        cutframes = ctrl.run_algorithm(algo_id, show_graph)

        self.set_progress(self.get_progress() + 5)

        # Ausgabe der zu schneidenden Frames
        for x in range(0, len(cutframes)):
            self.console_out("Cut-Frame : " + str(cutframes[x]))

        # Videocutter
        cutter = CutterController(self.filepaths, cutframes, 29)
        cutter.cut('../export/video/')
        self.set_progress(100)

        self.console_out("Processing Complete!")

        # Anzeige von Finish Fenster
        self.show_complete_window()


    def save_file(self):
        # Hole Pfad aus Filebrowser
        path = filedialog.asksaveasfilename(
            initialfile="output.avi",
            filetypes= [("AVI files", "*.avi")]
        )

        if (path != ''):
            shutil.move('../export/video/output.avi',path)

        self.quit()



    def quit_thread(self):
        self.console_out("[Status]: Shutdown application... Goodbye Butterfly")
        print('[Status]: Start shutting down the main thread...')

        # Beendet OpenPose
        if not self.__openPose == False:
            self.__openPose.kill()
