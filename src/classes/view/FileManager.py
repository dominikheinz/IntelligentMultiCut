from shutil import copyfile


class FileManager:
    __import_path = ""
    __export_path = ""


    def __init__(self, imp, exp):
        self.__import_path = imp
        self.__export_path = exp


    # kopiert Dateien von einem Ort zum anderen
    def copy(self):
        try:
            copyfile(self.__import_path, self.__export_path)
        except IOError:
            print("Kann nicht nach Zielort schreiben!\n")

