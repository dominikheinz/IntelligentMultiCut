from src.classes.core.Base import Base
import numpy as np
import cv2
import pathlib
import os


class Error(Exception):
   # Base Klasse für exceptions
   pass

class NoTuplesReceived(Error):
   # wenn die Tupel-Liste leer ist
   pass

class NoSourceFound(Error):
   # wenn die Quellpfad-Liste leer ist
   pass


class CutterController(Base):
    # eine Liste an Video-Quellpfaden
    __source_path = []
    # die Ausgabepfad(e) inklusive Name für das geschnittene Video (ohne Dateiendung)
    __output_path = []
    # speichert OpenCV Reader-Objekte (Objekte, aus denen Frames extrahiert werden)
    __reader_objects = []
    # speichert OpenCV Writer-Objekte (Objekte, in die Frames geschrieben werden)
    __writer_objects = []
    # eine Liste von Tupeln, die die Schneideinformationen enthalten
    __cut_info = [()]
    # Bilder pro Sekunde (Framerate)
    __frame_rate = 0
    # definiert den Codec für das Ausgabevideo
    __codec = ""
    # definiert die Auflösung für das Ausgabevideo
    __res = ()


    # Konstruktor von CutterController
    def __init__(self, path_in, info, fps):
        self.__source_path = path_in
        self.__cut_info = info
        self.__frame_rate = fps

        # holt den Codec aus der Config
        self.__codec = cv2.VideoWriter_fourcc(*self.config.get("video_codec"))

        # holt die Auflösung aus der Config
        self.__res = (self.config.get("video_width"), self.config.get("video_height"))


    # wirft die Anzahl an Quellpfaden zurück
    def get_num_of_src(self):
        return len(self.__source_path)


    # wirft die Anzahl an Zielpfaden zurück
    def get_num_of_out(self):
        return len(self.__output_path)


    # wirft die Anzahl an Tupeln zurück
    def get_num_of_tuples(self):
        return len(self.__cut_info)


    # initialisiert Reader- und Writer-Objekte, um Frames zu extrahieren und zu schreiben
    def open_reader_writer(self):
        try:
            if self.get_num_of_tuples() == 0:
                raise NoSourceFound
        except NoSourceFound:
            print("No source video was found! Source path list is empty!")

        # erstellt Reader-Objekte
        for reader_cnt in range(0, self.get_num_of_src()):

            self.__reader_objects.append(cv2.VideoCapture(self.__source_path[reader_cnt]))
            self.__reader_objects[reader_cnt].open(self.__source_path[reader_cnt])

        # erstellt Writer-Objekte
        for writer_cnt in range(0, self.get_num_of_out()):

            #print(self.__output_path[0])
            self.__writer_objects.append(cv2.VideoWriter())
            self.__writer_objects[writer_cnt].open(self.__output_path[writer_cnt], self.__codec, self.__frame_rate, self.__res)


    # Destruktor für Reader- und Writer-Objekte
    def close_reader_writer(self):

        # zerstört alle Reader-Objekte
        for reader_cnt in range(0, self.get_num_of_src()):
            self.__reader_objects[reader_cnt].release()

        # zerstört alle Writer-Objekte
        for writer_cnt in range(0, self.get_num_of_out()):
            self.__writer_objects[writer_cnt].release()

        cv2.destroyAllWindows()


    # Methode, die das eigentliche Schneiden der Videos durchführt
    def cut(self,output_path):

        try:
            if len(self.__cut_info) == 0:
                raise NoTuplesReceived
        except NoTuplesReceived:
            print("No cut tuples received! Cut tuple list is empty!")

        path = pathlib.Path(os.path.abspath(output_path))
        path.mkdir(
            parents = True,
            exist_ok = True
        )

        self.__output_path = [output_path+"output.avi"]

        self.open_reader_writer()

        tuples_counter = 0 # das momentan betrachtete Tupel
        frame_counter = 0 # der momentan betrachtete Frame
        end_of_file = False

        while not end_of_file:

            # Boundary check
            if tuples_counter < self.get_num_of_tuples():

                # wechselt das betrachtete Tupel
                # vergleicht aktuellen Frame mit Wert aus den Cut-Tupel
                if frame_counter == self.__cut_info[tuples_counter][1]:
                    tuples_counter += 1

            # geht alle Kameraperspektiven durch
            for reader_cnt in range(0, len(self.__reader_objects)):

                # sucht nach der aktuell zu zeigenden Kamera
                # zeigt und schreibt den entsprechenden Frame
                if (self.__cut_info[tuples_counter - 1][0] == reader_cnt):
                    ret, frame = self.__reader_objects[reader_cnt].read()

                    # falls aktueller Frame nicht leer ist
                    if ret:
                        # fix für inkompatible Auflösungen
                        resized_frame = cv2.resize(frame, self.__res)

                        if(self.config.get("display_cutterpreview")):
                            cv2.imshow('SundiVegas Pro does the work for you!', resized_frame)
                        self.__writer_objects[0].write(resized_frame)
                        print('[DEBUG] ACTIVE!', 'Frame:', frame_counter, 'Cam:', reader_cnt)

                    # falls aktueller Frame leer ist (end of file)
                    else:
                        end_of_file = True

                # überspringt die Frames der anderen Kameras
                else:
                    self.__reader_objects[reader_cnt].grab()
                    #print('[DEBUG] SKIP!', 'Frame:', frame_counter, 'Cam:', reader_cnt)

            # inkrementiert den frame_counter
            frame_counter += 1
            '''
            if cv2.waitKey(1) & 0xFF == ord('q'):
                #print('[DEBUG] FINSHED!')
                break
            '''

        self.close_reader_writer()


    def clap_sync(self,output_path):
        # lege einen neuen Ordner an, wenn der Zielordner nicht vorhanden ist
        path = pathlib.Path(os.path.abspath(output_path))
        path.mkdir(
            parents = True,
            exist_ok = True
        )

        for tuple in range(0, len(self.__cut_info)):
            #self.__output_path[tuple] = output_path + self.__cut_info[0] + '.avi'
            self.__output_path.append(output_path + self.__cut_info[tuple][0] + '.avi')
        #print(self.__output_path)

        self.open_reader_writer()

        # geht alle Quellvideos durch
        for reader_cnt in range(0, len(self.__reader_objects)):

            # holt den gewünschten Start-Zeitpunkt des aktuellen Videos
            clap_frame = int(self.__cut_info[reader_cnt][1] * self.__frame_rate)

            frame_counter = 0  # der momentan betrachtete Frame
            end_of_file = False

            while not end_of_file:

                # sobald der Clap einsetzt, wird geschrieben
                if(frame_counter >= clap_frame):
                    ret, frame = self.__reader_objects[reader_cnt].read()
                    if ret:
                        resized_frame = cv2.resize(frame, self.__res)

                        if (self.config.get("display_cutterpreview")):
                            cv2.imshow('SundiVegas Pro syncs video nr ' + str(reader_cnt) + ' for you!', resized_frame)
                        self.__writer_objects[reader_cnt].write(resized_frame)
                        #print('[DEBUG] ACTIVE!', 'Frame:', frame_counter, 'Cam:', reader_cnt)

                    # sobald das Video sein Ende erreicht hat, endet die innere Schleife
                    else:
                        end_of_file = True
                        #print('[DEBUG] DONE!', 'Frame:', frame_counter, 'Cam:', reader_cnt)

                # solange der Clap noch nicht eingesetzt hat, überspringe frame
                else:
                    self.__reader_objects[reader_cnt].grab()
                    #print('[DEBUG] SKIP!', 'Frame:', frame_counter, 'Cam:', reader_cnt)

                # inkrementiert den frame_counter
                frame_counter += 1
                '''
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    #print('[DEBUG] FINSHED 1 SYNC!')
                    break
                '''

        self.close_reader_writer()

        return self.__output_path