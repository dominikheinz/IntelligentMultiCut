from subprocess import call


class AudioController:
    # der Pfad des Cutter-Ausgabevideos
    __source_video = ''
    # der Pfad des längsten Sync-Audiofiles
    __source_audio = ''
    # der zusammengesetzte Konsolenbefehl, um Video und Audio zu konkatenieren
    __shell_command = ''


    # Konstruktor
    def __init__(self, src_vid, src_audio):
        self.__source_video = src_vid
        self.__source_audio = src_audio


    def add_audio(self):
        self.__shell_command = 'ffmpeg -i ' + self.__source_video + ' -i ' + self.__source_audio + ' -codec copy -shortest ' + self.__source_video
        print(self.__shell_command)
        call(self.__shell_command, shell=True)