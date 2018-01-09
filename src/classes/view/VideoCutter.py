from src.lib.ffmpeg import *
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, clips_array, vfx


class VideoCutter:
    # Quellpfade werden als string in einem Vektor gespeichert.
    __source_path = []
    # String mit dem Ausgabepfad
    __output_path = ""
    # Vektor mit zwei Tuplen (file index, frame number)
    __cut_info = [()]
    # Frames pro Sekunde
    __frame_rate = 0


    # Konstruktor des VideoCutters
    def __init__(self, path_in, path_out, info, fps):
        self.__source_path = path_in
        self.__output_path = path_out
        self.__cut_info = info
        clip = VideoFileClip(self.__source_path[0])
        self.__frame_rate = clip.fps


    # Destructor des VideoCutters
    def __del__(self):
        print("Destructor does its job\n")


    # Fügt subclips zu einem neuen clip zusammen.
    def cut(self):
        # Speichert subclips mit der gleichen Länge in einem Array
        subclips = []

        # Durchläuft den Vektor der Tuples
        for cnt in range(0, len(self.__cut_info)):

            # Index des Quellpfades des Tuples
            source_index = self.__cut_info[cnt][0]

            # Berechnet den Zeitpunkt, wann die Kameraperspektive gewechselt werden muss
            start_frame = self.__cut_info[cnt][1] / self.__frame_rate

            print(cnt)

            # Ausnahme für den letzten subclip --> läuft zuende
            if cnt == len(self.__cut_info) - 1:
                subclips.append(VideoFileClip(self.__source_path[source_index]).subclip(start_frame))

            # Erstellt und fügt neue subclips in der richtigen Länge hinzu
            else:
                end_frame = self.__cut_info[cnt + 1][1] / self.__frame_rate
                subclips.append(VideoFileClip(self.__source_path[source_index]).subclip(start_frame, end_frame))

        # Fügt subclips zusammen
        final_clip = concatenate_videoclips(subclips)
        # Erstellt eine .mp4 Datei
        final_clip.write_videofile(self.__output_path + ".mp4")


    # Erstellt ein Array für die Videospuren (only for exactly 3 clips)
    def create_clip_array(self):
        subclips_amount = len(self.__source_path)

        if subclips_amount != 3:
            print("Only works with exactly 3 clips!\n")
        else:
            subclips = []

            for cnt in range(0, 3):
                current_clip = VideoFileClip(self.__source_path[cnt])

                # Appends clips to the subclips vector
                subclips.append(current_clip)

            final_clip_array = clips_array([[subclips[0], subclips[1], subclips[2]]])
            final_clip_array.write_videofile("arrayTest.mp4")
            os.startfile("arrayTest.mp4")


# Debug function - might be changed, was supposed to work on local project
def test_cut():
    test_src = ["Clip3_BaumRunner_Cam1.mp4", "Clip3_BaumRunner_Clip2.mp4", "Clip3_BaumRunner_Clip3.mp4"]
    out = "test_out"
    dummy_tuples = [(0, 0 * 30), (2, 5 * 30), (1, 11 * 30), (0, 17 * 30)]
    fps = 30

    Test = VideoCutter(test_src, out, dummy_tuples, fps)
    Test.cut()

