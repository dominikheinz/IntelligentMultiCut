from src.classes.controllers.GraphHelper import GraphHelper
from src.classes.core.Base import Base


class PoseController(Base):
    def __init__(self, all_frames):
        self.__allFrames = all_frames
        self.__min_precision = 0.2
        self.__default_cam = 0
        self.__threshold = 26  # Kamerawechsel nicht schneller als 26 fps

    # Gibt die Anzahl der erkannten Leute in einem Frame zurueck
    def count_people_in_frame(self, frame_id, cam_id):
        return len(self.__allFrames[frame_id].get_camera(cam_id)["people"])

    # Gibt ein array mit den nodes aller bodyparts in einem frame fuer alle Personen zurueck
    def get_body_nodes(self, frame_id, cam_id):
        return self.__allFrames[frame_id].get_camera(cam_id)["people"]

    # Gibt den errechneten score fuer eine Kamera und einen Frame zurueck
    def calc_pose_score(self, frame_id, cam_id, PersonNr):

        person_arr = self.get_body_nodes(frame_id, cam_id)

        current_precision = 0
        current_precision += person_arr[PersonNr]["left_eye"][2]
        current_precision += person_arr[PersonNr]["right_eye"][2]
        current_precision += person_arr[PersonNr]["nose"][2]
        current_precision += person_arr[PersonNr]["neck"][2]
        current_precision += person_arr[PersonNr]["left_shoulder"][2]
        current_precision += person_arr[PersonNr]["left_elbow"][2]
        current_precision += person_arr[PersonNr]["left_wrist"][2]
        current_precision += person_arr[PersonNr]["right_shoulder"][2]
        current_precision += person_arr[PersonNr]["right_elbow"][2]
        current_precision += person_arr[PersonNr]["right_wrist"][2]
        current_precision += person_arr[PersonNr]["left_hip"][2]
        current_precision += person_arr[PersonNr]["left_knee"][2]
        current_precision += person_arr[PersonNr]["left_foot"][2]
        current_precision += person_arr[PersonNr]["right_hip"][2]
        current_precision += person_arr[PersonNr]["right_knee"][2]
        current_precision += person_arr[PersonNr]["right_foot"][2]
        current_precision /= 15

        precision = current_precision

        if precision > self.__min_precision:
            return precision
        else:
            return 0

    def run_pose_algorithm(self, show_graph):
        result_array = []
        score_array = []

        # Iteriere alle frames
        for x in range(0, len(self.__allFrames)):
            best_precision = 0
            # Iteriere alle cams
            for z in range(0, self.__allFrames[x].get_camera_amount()):
                # Analysiere aktuellen frame
                precision = self.calc_pose_score(x, z, 0)
                score_array.append((z, precision))

                print("Frame: ", x, "Cam: ", z, "Score: ", precision)

        gh = GraphHelper(score_array, self.__allFrames)
        result_array = gh.smooth_for_algo()

        if show_graph:

            gh.show_algodata_graph(True, "Singleperson Score Curve")
        return result_array
