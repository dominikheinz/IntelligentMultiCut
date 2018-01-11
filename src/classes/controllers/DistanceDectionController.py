import math
import tkinter as Tk

from src.classes.controllers.GraphHelper import GraphHelper
from src.classes.view.GraphViewer import GraphViewer


class DistanceDetectionController:
    __frames = []
    __frame_count = 0
    __factor_eye_eye_neck = 1.0
    __factor_eye_neck = 0.75
    __factor_neck_nose = 0.5

    def __init__(self, all_frames):
        self.__frames = all_frames
        self.__frame_count = len(self.__frames)
        self.__threshold = 8  # Kamerawechsel nicht schneller als 26 fps

    # Gibt die Anzahl der erkannten Leute in einem Frame zurueck
    def count_people_in_frame(self, frame_id, cam_id):
        return len(self.__frames[frame_id].get_camera(cam_id)["people"])

    # Returns an array of all body nodes
    def get_bodyparts(self, frame_id, cam_id):
        return self.__frames[frame_id].get_camera(cam_id)["people"]

    # Calculates the difference between two points
    def calc_node_distance(self, node1_x, node2_x, node1_y, node2_y):
        return math.sqrt(((node1_x - node2_x) ** 2) + ((node1_y - node2_y) ** 2))

    # Verifies if one of the node coords is 0
    def verify_nodes(self, node_x, node_y):
        if node_x == 0 or node_y == 0:
            return 0
        else:
            return 1

    def middle_point_line(self, node_x_1, node_x_2, node_y_1, node_y_2):
        x_value = ((node_x_1 + node_x_2) / 2)
        y_value = ((node_y_1 + node_y_2) / 2)
        return [x_value, y_value]

    # Calculates the distance from the neck node between the point between both hip nodes
    def calc_distance_score(self, body_arr, PersonNr):

        l_eye_x = body_arr[PersonNr]["left_eye"][0]
        l_eye_y = body_arr[PersonNr]["left_eye"][1]
        r_eye_x = body_arr[PersonNr]["right_eye"][0]
        r_eye_y = body_arr[PersonNr]["right_eye"][1]
        neck_x = body_arr[PersonNr]["neck"][0]
        neck_y = body_arr[PersonNr]["neck"][1]
        nose_x = body_arr[PersonNr]["nose"][0]
        nose_y = body_arr[PersonNr]["nose"][1]

        left_eye_recognized = self.verify_nodes(l_eye_x, l_eye_y)
        right_eye_recognized = self.verify_nodes(r_eye_x, r_eye_y)
        eyes_recognized = left_eye_recognized and right_eye_recognized
        neck_recognized = self.verify_nodes(neck_x, neck_y)
        nose_recognized = self.verify_nodes(nose_x, nose_y)

        if eyes_recognized and neck_recognized:
            return self.calc_distance_eyes_neck(l_eye_x, l_eye_y, neck_x, neck_y, r_eye_x, r_eye_y)
        elif (left_eye_recognized == 1 and right_eye_recognized == 0) and neck_recognized:
            return self.calc_distance_lefteye_neck(l_eye_x, l_eye_y, neck_x, neck_y)
        elif (left_eye_recognized == 0 and right_eye_recognized == 1) and neck_recognized:
            return self.calc_distance_righteye_neck(neck_x, neck_y, r_eye_x, r_eye_y)
        else:
            if nose_recognized and neck_recognized:
                return self.calc_distance_neck_nose(neck_x, neck_y, nose_x, nose_y)
            else:
                # Wenn keine Nodes erkannt, return 0 als score
                print("Failed to detect body nodes")
                return 0

    def calc_distance_neck_nose(self, neck_x, neck_y, nose_x, nose_y):
        nose_neck_distance = self.calc_node_distance(nose_x, neck_x, nose_y, neck_y) * self.__factor_neck_nose
        print("Nose-Neck Distance : ", nose_neck_distance)
        return nose_neck_distance

    def calc_distance_righteye_neck(self, neck_x, neck_y, r_eye_x, r_eye_y):
        r_eye_neck_distance = self.calc_node_distance(r_eye_x, neck_x, r_eye_y, neck_y) * self.__factor_eye_neck
        print("Right-Eye-Neck Distance : ", r_eye_neck_distance)
        return r_eye_neck_distance

    def calc_distance_lefteye_neck(self, l_eye_x, l_eye_y, neck_x, neck_y):
        l_eye_neck_distance = self.calc_node_distance(l_eye_x, neck_x, l_eye_y, neck_y) * self.__factor_eye_neck
        print("Left-Eye-Neck Distance : ", l_eye_neck_distance)
        return l_eye_neck_distance

    def calc_distance_eyes_neck(self, l_eye_x, l_eye_y, neck_x, neck_y, r_eye_x, r_eye_y):
        eye_middle_x, eye_middle_y = self.middle_point_line(l_eye_x, r_eye_x, l_eye_y, r_eye_y)
        eye_middle_neck_distance = self.calc_node_distance(eye_middle_x, neck_x, eye_middle_y,
                                                           neck_y) * self.__factor_eye_eye_neck
        print("Eye-Eye-Neck Distance : ", eye_middle_neck_distance)
        return eye_middle_neck_distance


    def run_distance_algorithm(self, show_graph):
        best_cam = 0
        result_array = []
        score_array = []
        solution2 = []

        # Iteriere alle frames
        for x in range(0, self.__frame_count):
            best_precision = 0
            # Iteriere alle cams
            for z in range(0, self.__frames[x].get_camera_amount()):

                if self.count_people_in_frame(x, z) != 0:
                    # Errechne distance score für einen frame
                    print("Frame ", x, " cam ", z)
                    bodyparts = self.get_bodyparts(x, z)
                    precision = self.calc_distance_score(bodyparts, 0) # 0 für die Erst-beste Person
                else:
                    precision = 0

                score_array.append((z, precision))
                # Vergleiche aktuelle Praezision mit bester Praezision

                if (precision > best_precision):
                    best_precision = precision
                    best_cam = z

            #result_array.append((best_cam, x))

        gh = GraphHelper(score_array, self.__frames)
        result_array = gh.smooth_for_algo()
        if show_graph:

            gh.show_algodata_graph(True, "Distance Score Curve")

        return result_array
