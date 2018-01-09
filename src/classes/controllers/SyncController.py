#@todo Prüfe auf ffmpeg installation, ob vorhanden

import subprocess
import os
from src.classes.core.Base import Base
from pydub import AudioSegment
class SyncController(Base):

    def __init__(self,filepaths):
        self.videos = filepaths
        self.tmp_dir = "../import/tmp"
        self.result_tupel = []
        self.threshold = self.config.get("db_threshold")

    # Extrahiert die Audiospuren der Videos
    def extract_audio(self):

        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

        # Iteriert durch alle eingelesen Videos
        for video in self.videos:
            output_audio = self.extract_name(video)
            audio_path = os.path.abspath(self.tmp_dir + "/" + output_audio + ".mp3")
            command = "ffmpeg -y -i  \"" + video + "\"  -f mp3 -ab 192000 -vn \""+ audio_path +"\" -loglevel quiet"
            subprocess.call(command, shell=True)

    # Erstellt Audio Datei aus der extrahierten Tonspur
    def extract_name(self,path):
        filename = path.split("/")
        filename = filename[-1]

        filename = os.path.splitext(filename)[0]
        return filename

    # Analysiert die extrahierte Audiospur
    def audio_analyse(self):

        self.extract_audio()

        # Durchläuft die Audiospuren zu den dazugehörigen Videospuren
        for video in self.videos:
            filename = self.tmp_dir + "/" + self.extract_name(video) + ".mp3"
            sound = AudioSegment.from_mp3(filename)

            counter = 0
            normalize_sound = sound.apply_gain(-sound.max_dBFS)

            for frame in normalize_sound:

                if(frame.dBFS > self.threshold):
                    self.result_tupel.append((self.extract_name(video),counter/1000))
                    break

                counter += 1

        return self.result_tupel