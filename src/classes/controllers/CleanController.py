from src.classes.core.Base import Base
import subprocess,os
import shutil

class CleanerController(Base):

    # Löscht alle generierten JSON Dateien vor jedem neuen Prozess
    def clean_workspace(self):

        if not self.config.get("debug"):
            if os.path.isdir("../export/json"):
                #subprocess.call("rmdir \"../export/json\" /s /q",shell=True)
                shutil.rmtree('../export/json',ignore_errors=True)
            if os.path.isdir("../import/tmp"):
                 #subprocess.call("rmdir \"../import/tmp\" /s /q", shell=True)
                shutil.rmtree('../import/tmp',ignore_errors=True)
            if os.path.isdir("../import/videos"):
                #subprocess.call("rmdir \"../import/videos\" /s /q", shell=True)
                shutil.rmtree('../import/videos',ignore_errors=True)


        while (os.path.isdir("../export/json") and os.path.isdir("../import/tmp") and os.path.isdir("../import/videos")):
            pass