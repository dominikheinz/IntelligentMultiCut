from moviepy.editor import *
from PIL import Image
from PIL import ImageTk
import cv2


class ThumbnailCreator:
    __time_code = ""

    def __init__(self, src, out, time):
        self.__source_path = src
        self.__output_path = out
        self.__time_code = time

    def __init__(self, src, time):
        self.__source_path = src
        self.__output_path = ""
        self.__time_code = time


    def export_thumbnail(self):
        input_video = VideoFileClip(self.__source_path)
        input_video.save_frame(self.__output_path, t=self.__time_code)

    def get_thumbnailTK(self):

        # Mit Hilfe von OpenCV wird ein Thumbnail erstellt.
        cap = cv2.VideoCapture(self.__source_path)
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(frame)

        # Thumbnail wird in Tkinter Image umgewandelt.
        return ImageTk.PhotoImage(image=img)



# baum = ThumbnailCreator("../../../import/videos/test.avi", "../../../import/videos/thumbnailtest.jpg", "00:00:03")
# baum.export_thumbnail()