from src.classes.controllers.GraphHelper import GraphHelper
from src.classes.core.Base import Base
from src.classes.controllers.DistanceDectionController import DistanceDetectionController
from src.classes.controllers.PoseController import PoseController


class MultiPersonController(Base):
    __frames = []
    __frame_count = 0

    def __init__(self, frames):
        self.__frames = frames
        self.__frame_count = len(self.__frames)

    def get_amount_of_people(self, frame_id, cam_id):
        return len(self.__frames[frame_id].get_camera(cam_id)["people"])

    def run_multiperson_most_people(self, show_graph):

        result_arr = []
        score_array = []

        # Gehe durch alle frames
        for x in range(0, self.__frame_count):

            most_people = 0

            # Gehe durch alle Cams
            for y in range(0, self.__frames[x].get_camera_amount()):

                # Personen werden gezählt in der Kamera in diesem Frame
                people_count = self.get_amount_of_people(x, y)
                person_counter = 0

                # springe hier rein wenn die personen-anzahl über 0 fällt
                if people_count != 0:
                    po = PoseController(self.__frames)

                    # Gehe durch alle Personen in der Kamera berechne den score und zähle die tatsächlichen Personen score(<0,1)
                    for z in range(0, people_count):

                        person_value = po.calc_pose_score(x,y,z)

                        # zähle alle personen
                        if(person_value != 0):
                            person_counter += 1

                print("People: ", person_counter)
                if person_counter > most_people:
                    most_people = person_counter

                # Score_array für den graphen
                score_array.append((y, person_counter))

        gh = GraphHelper(score_array, self.__frames)
        result_arr = gh.smooth_for_algo()

        if show_graph:
            # Grapherstellung
            gh.show_algodata_graph(True, "Multiperson Score Curve")

        return result_arr

    def run_multiperson_close_up(self, show_graph):
        result_arr = []
        score_array = []

        # Gehe durch alle frames
        for x in range(0, self.__frame_count):

            bestscore_from_all_cams = 0

            # Gehe durch alle Cams
            for y in range(0, self.__frames[x].get_camera_amount()):

                bestscore_for_this_cam = 0
                temp = 0

                people_in_cam = self.get_amount_of_people(x, y)

                # Keine Person -> Score = 0
                if people_in_cam != 0:
                    dc = DistanceDetectionController(self.__frames)
                    bodyparts = dc.get_bodyparts(x, y)

                    # Gehe durch alle Personen in der Kamera
                    for z in range(0, people_in_cam):

                        temp = dc.calc_distance_score(bodyparts, z)

                        # hole den besten Score für diese Kamera
                        if temp > bestscore_for_this_cam:
                            bestscore_for_this_cam = temp


                    print("Frame: ", x, "Cam: ", y, "Personen: ", people_in_cam, "CamScore: ", bestscore_for_this_cam)
                    score_array.append((y, bestscore_for_this_cam))

                else:
                    bestscore_from_all_cams = 0
                    bestscore_for_this_cam = 0

        gh = GraphHelper(score_array, self.__frames)
        result_arr = gh.smooth_for_algo()

        if show_graph:
            gh.show_algodata_graph(True, "Multiperson Score Curve")

        return result_arr

    # Wähle einen multiperson-algo
    def run_multiperson_algorithm(self, mp_algo_id, show_graph):
        if mp_algo_id == 0:
            return self.run_multiperson_most_people(show_graph)
        elif mp_algo_id == 1:
            return self.run_multiperson_close_up(show_graph)
        else:
            print("Invalid algorithm id")
            return None
