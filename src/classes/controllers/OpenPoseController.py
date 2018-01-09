from src.classes.core.Base import Base
import os
import pathlib
import subprocess
import psutil
import time

class OpenPoseController(Base):

    def __init__(self):
        self.video_counter = 0
        self.running_processes = []

        self.__check_installation()


    def process(self, filepaths):

        for file in filepaths:

            # Wartet bis ein neuer Slot für einen weiteren Prozess frei wird.
            while (not self.__max_processes()):
                time.sleep(0.1)

            print("[OpenPose]:  Analyse new video")

            filename = file.split("/")
            filename = filename[-1]

            # Erstellt einen neuen Ordner, falls bereits keiner angelegt ist.
            path = pathlib.Path(os.path.abspath("../export/json/" + str(self.video_counter)))
            path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            # Bereitet alle notwendigen Parameter zum Ausführen vor

            display = ""
            if not self.config.get("display_openpose"):
                display = " --no_display"

            face_tracking = ""
            if self.config.get("openpose_facetracking"):
                    face_tracking = " --face"

            file = os.path.abspath(file)

            param = " --video " + file + " --write_keypoint_json " + os.path.abspath(
                "../export/json/" + str(self.video_counter)) + display + face_tracking

            # Führt die OpenPose Demo aus mit allen zur Verfügung gestellten Parametern.
            self.__execute__(param)
            
            # Erhöht den Video Counter, um einen neuen Ordner für weitere Videospuren mit einem anderen Namen erstellen zu können.
            self.video_counter += 1

        # Wartet bis alle OpenPose Prozesse beendet sind.
        while (self.is_running()):
            time.sleep(0.5)

    def __execute__(self, param):
        # Führt OpenPose Demo aus und liest die dazugehörigen Parameter ein.
        self.running_processes.append(subprocess.Popen("cd lib/openpose & \"bin/OpenPoseDemo.exe\"" + param, shell=True))

    def __max_processes(self):

        # Berechnet die Anzahl der offenen Open Pose Prozesse.
        amount_of_cpuCores = psutil.cpu_count()
        amount_of_processes = round(amount_of_cpuCores / 2, 0)

        # Wenn die CPU Auslastung, über 20 ist, wird kein neuer Prozess mehr gestartet.
        max_cpu_usage = 20

        #print("[CPU]: ", psutil.cpu_percent(interval=0.5), "%")

        # Prüft, ob die CPU Auslastung zu hoch ist.
        running = 0
        for process in self.running_processes:

            # if the process is alive
            if (process.poll() == None):
                running += 1

        if(running <= amount_of_processes and psutil.cpu_percent(interval=0.5) <= max_cpu_usage):
            return True
        else:
            return False


    def is_running(self):

        # Überprüft, ob OpenPose Prozesse laufen.
        current_process = psutil.Process()
        children = current_process.children(recursive=True)

        for child in children:
            if ("OpenPoseDemo" in child.name() or "cmd" in child.name()):
                return True

        return False


    def kill(self):

        # no shared scope
        #OpenPoseController.openPoseProcess.kill()

        # Beendet alle OpenPose und Kind Prozesse
        current_process = psutil.Process()
        children = current_process.children(recursive=True)

        for child in children:
            print("[Status]: Kill " + child.name())
            p = psutil.Process(child.pid)
            p.terminate()



    def __check_installation(self):

        # check open pose
        if not (os.path.isfile("lib/openpose/bin/OpenPoseDemo.exe")):
            print("[Error]: OpenPose isn't installed. Please install OpenPose at src/lib/openpose/bin/OpenPoseDemo.exe")
            exit(-1)
