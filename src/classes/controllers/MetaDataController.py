from src.classes.core.Base import Base
from src.classes.models.FrameMetaData import FrameMetaData
from pprint import pprint
import json
import sys
import os


class MetaDataController(Base):
    def __init__(self):

        # Initialisiert das base Frame Array
        self.frames = []

        # Sammelt die von OpenPose generierten Daten aus den JSON Files
        self.__collect_cameras__()


    def get_frames(self):
        return self.frames


    def __collect_cameras__(self):

        # Durchsucht alle Ordner in denen sich Video Dateien befinden
        for subdir, dirs, files in os.walk("../export/json/"):

            # zählt die aktuellen Frames für die bestimmten Kameras hoch
            frame_counter = 0

            # Iteriert durch alle JSON meta data files
            for file in sorted(files):

                # Prüft, ob das Frame Objekt von einer anderen Kamera erfasst wurde
                if frame_counter < len(self.frames):

                    # Fügt Kamera meta data einem existierenden Frame Objekt hinzu
                    data = self.__read_file__(os.path.join(subdir, file))

                    if(data):
                        self.frames[frame_counter].add_camera_data(data)
                    else:
                        # Überspringen, wenn die aktuelle Datei keine JSON File ist.
                        continue

                else:
                    # Aktuell kein Frame Objekt für den aktuellen Frame vorhanden.

                    # Weist den Kamera Meta Daten ein neues Frame Objket zu.
                    data = self.__read_file__(os.path.join(subdir, file))

                    if (data):
                        # Neues Frame Objekt wird erstellt
                        self.frames.append(FrameMetaData())

                        # Fügt Meta Daten hinzu
                        self.frames[frame_counter].add_camera_data(data)
                    else:
                        # Überspringen, wenn die aktuelle Datei keine JSON File ist.
                        continue

                # Erhöht den Frame Counter um 1.
                frame_counter += 1


    def __read_file__(self, filename):

        # Überprüft, ob die angegebene Datei eine JSON Datei ist.
        if(filename.endswith(".json")):

            # Versucht JSON Datei zu öffen und auszuführen
            try:
                with open(filename) as data_file:
                    parsed_data = json.load(data_file)

                    if parsed_data["version"] == 1.0:
                        return parsed_data
                    else:
                        print("[Error]: The metadata file: " + filename + " isn't supported. We need version 1.0")
                        return 0
            except Exception:
                print("[Error]: Can't open JSON file for frame " + filename)
        else:
            return 0





