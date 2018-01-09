import ffmpeg
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, clips_array, vfx


class VideoCutter:
    __sourcePath = []   # A vector to store source paths as strings
    __outputPath = ""   # A string containing the output path
    __clipJumpInfo = [()]   # A vector of 2-tuples (file index, frame number)
    __frameRate = 0   # Frames per second

    def __init__(self, path_in, path_out, jmp, fps): # Constructor of VideoCutter
        self.__sourcePath = path_in
        self.__outputPath = path_out
        self.__clipJumpInfo = jmp
        self.__frameRate = fps

    def __del__(self):  # Destructor of VideoCutter
        print("Destructor does its job\n")

    def cut(self): # Cut method: concatenates subclips to a new clip
        subclips = [] # Collects subclips that are already cut into the right length

        for cnt in range(0, len(self.__clipJumpInfo)):  # Traverses the vector of tuples

            sourceIndex = self.__clipJumpInfo[cnt][0]   # Gets the index of the tuple's source path
            startFrame = self.__clipJumpInfo[cnt][1] / self.__frameRate     # Calculates the time when to switch camera perspective

            if (cnt == len(self.__clipJumpInfo) - 1):   # Exception for last subclip
                subclips.append(VideoFileClip(self.__sourcePath[sourceIndex]).subclip(startFrame))

            else:   # Creates and adds subclips in the appropriate length
                endFrame = self.__clipJumpInfo[cnt + 1][1] / self.__frameRate
                subclips.append(VideoFileClip(self.__sourcePath[sourceIndex]).subclip(startFrame, endFrame))

        final_clip = concatenate_videoclips(subclips)   # Connects all subclips
        final_clip.write_videofile(self.__outputPath + ".mp4")  # Writes an .mp4 file

    def createClipArray(self):  # Creates an array of input clips (only for exactly 3 clips)
        subclipsAmount = len(self.__sourcePath)

        if (subclipsAmount != 3):
            print("Only works with exactly 3 clips!\n")
        else:
            subclips = []

            for cnt in range(0, 3):
                currentClip = VideoFileClip(self.__sourcePath[cnt])
                subclips.append(currentClip)    # Appends clips to the subclips vector

            finalClipArray = clips_array([[subclips[0], subclips[1], subclips[2]]])
            finalClipArray.write_videofile("arrayTest.mp4")
            os.startfile("arrayTest.mp4")


def test_func(): # Debug function
    testSrc = ["Clip1_Cam1.mp4", "Clip1_Cam2.mp4", "Clip1_Cam3.mp4"]
    out = "test_out"
    frame_jmps = [(0, 0 * 30), (2, 5 * 30), (1, 11 * 30), (0, 17 * 30)]
    fps = 30

    Test = VideoCutter(testSrc, out, frame_jmps, fps)
    Test.cut()
    # Test.createClipArray()


test_func()
