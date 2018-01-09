from shutil import copyfile

class filemanager:
    __importPath = ""
    __exportPath = ""

    def __init__(self, imp, exp):
        self.__importPath = imp
        self.__exportPath = exp

    def copy(self):
        try:
            copyfile(self.__importPath, self.__exportPath)
        except IOError:
            print("Kann nicht nach Zielort schreiben!\n")