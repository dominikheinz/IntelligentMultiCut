import json
import os.path
import sys

class Config:
    json_path = ""
    __data = ""

    def __init__(self, path):
        self.__json_path = path

        # lesen und analysieren der Config Datei
        self.read_file()

    def get_json_path(self):
        return self.__json_path

    def read_file(self):

        # Versucht Config Datei zu lesen und zu analysieren
        try:
            with open(self.__json_path) as data_file:

                # Analysiert JSON Datei
                self.__data = json.load(data_file)
            data_file.close()
        except Exception:
            print("[Error]: Config file not found")
            sys.exit(1)

    def get(self, key):
        return self.__data[key]

    def set(self,key,value):
        self.__data[key] = value

        # Speichert Änderungen in der Config Datei
        data_file = open(self.__json_path,"w+")
        data_file.write(json.dumps(self.__data,indent=4, sort_keys=True))
        data_file.close()

    def get_data(self):
        return self.__data