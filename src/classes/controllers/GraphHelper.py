from src.classes.view.GraphViewer import GraphViewer
from src.classes.controllers.SmoothController import SmoothController
from itertools import zip_longest
import tkinter as Tk

class GraphHelper:

    __cam_score_array = None

    def __init__(self, cam_arr, frames):
        self.__cam_score_array = cam_arr
        self.__frames = frames

    def show_algodata_graph(self, smooth, title):

        graph_arr = self.split_graph_array(self.__frames[0].get_camera_amount())
        root = Tk.Tk()
        app = GraphViewer(root, graph_arr, smooth, title)
        app.show_algorithm_graphs()
        app.master.title("GraphViewer")
        root.mainloop()

    def split_graph_array(self, cam_count):
        final = []
        for x in range(0, cam_count):
            temp = []
            for z in range(0, len(self.__cam_score_array)):
                if self.__cam_score_array[z][0] == x:
                    temp.append(self.__cam_score_array[z][1])
            final.append(temp)
        return final

    def smooth_for_algo(self):
        smooth_arr = []
        result_arr = []

        graph_arr = self.split_graph_array(self.__frames[0].get_camera_amount())

        for k in range(0, len(graph_arr)):
            x_val = list(range(len(graph_arr[k])))
            y_val = graph_arr[k]


            SC = SmoothController(x_val, y_val)
            y_val_smooth = SC.smooth()
            smooth_arr.append(y_val_smooth)

        result_arr = self.get_final_array_from_smoothed_data(smooth_arr)

        return result_arr



    def get_final_array_from_smoothed_data(self, smoothed_data):

        final_arr = []
        choosen_cam = 0
        loopcounter = 0

        for x in zip_longest(*smoothed_data, fillvalue=0):


            temp = 0
            best_cam_score = 0

            for y in range(len(x)):

                temp = x[y]
                if temp > best_cam_score:
                    best_cam_score = temp
                    choosen_cam = y

            print("FrameData: ", x, "ChoosenCam: ", choosen_cam)


            final_arr.append((choosen_cam, loopcounter))
            loopcounter += 1


            print("Best_cam_score: ", best_cam_score)

        return final_arr

