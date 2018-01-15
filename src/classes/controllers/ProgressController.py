import os
import time
from src.classes.core.Base import Base
import cv2

class ProgressController(Base):

    # Pfade aller eingelesenen Videodateien
    __source_paths = []

    # Anzahl der zu durchsuchenden Ordner
    __number_of_folders = 0

    # Pfad zu json Dateien
    __json_path = ""

    # Debug Modus zum testen ohne Videos
    __debug = 1

    # Anzahl erwarteter frames
    __total_files_expected=0

    # Zwischenspeichern von Dateien current und recent
    __folder_sizes=[]


    # Konstruktor : ProgressCalculator
    def __init__(self, gui,src = []):
        self.__source_paths = src
        self.__number_of_folders = len(self.__source_paths)
        self.__json_path = "../export/json/"
        self.gui = gui

    # berechne Prozentzahl
    def calculate_progress(self):
        total_files_counted=0
        folder_index = 0

        # hole erwartete Anzahl an Dateien
        for file in self.__source_paths:
            cap = cv2.VideoCapture(file)
            folder_files_expected = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.__total_files_expected += folder_files_expected
            self.__folder_sizes.append({'current':0,'recent':0})
        print("Total files expected: ",self.__total_files_expected)

        old_progress = self.gui.get_progress()
        while (total_files_counted < self.__total_files_expected):
            total_files_counted=0
            folder_index = folder_index % (self.__number_of_folders)

            # hole Liste aller Daten im aktuellen Ordner
            if os.path.isdir("../export/json/"+str(folder_index)):
                files = os.listdir(self.__json_path + str(folder_index))

                self.__folder_sizes[folder_index]['current'] = len(files)

                # berechne gesamte Prozentzahl und gebe sie aus

                if(self.__folder_sizes[folder_index]['current'] > self.__folder_sizes[folder_index]['recent']):
                    self.__folder_sizes[folder_index]['recent'] = self.__folder_sizes[folder_index]['current']

                for size in self.__folder_sizes:
                    total_files_counted+=size['recent']

                self.__current_progress = (total_files_counted) / self.__total_files_expected * 75
                #print("[ProgressController]: Current progress: " + str(self.__current_progress) + " percent")

                new_progress = old_progress + self.__current_progress

                if("set_progress" in dir(self.gui)):
                    self.gui.set_progress(new_progress)
                else:
                    exit(0)
            else:
                true = 1
                #print("Waiting for json folder: '"+str(folder_index)+"' to be created...")
            time.sleep(0.1)
            folder_index += 1