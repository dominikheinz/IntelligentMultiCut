from src.classes.controllers.GraphHelper import GraphHelper
from src.classes.core.Base import Base
from src.classes.controllers.DistanceDectionController import DistanceDetectionController


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
        choosen_cam = 0
        last_cam = 0
        last_cam_amount = 0
        score_array = []

        # Gehe durch alle frames
        for x in range(0, self.__frame_count):

            most_people = 0

            # Gehe durch alle Cams
            for y in range(0, self.__frames[x].get_camera_amount()):

                # Personen werden gezählt und Kamera mit den meisten wird choosen_cam
                people_count = self.get_amount_of_people(x, y)
                print("People: ", people_count)
                if people_count > most_people:
                    most_people = people_count
                    choosen_cam = y

                # Score_array für den graphen
                score_array.append((y, self.get_amount_of_people(x, y)))

            # Prüfe den Frame von der Kamera die zuletzt die beste war auf gleichheit der Menge an Kameras mit diesem frame
            if last_cam_amount == self.__frames[x].get_camera_amount():

                # Wenn Personen-Anzahl gleich groß ist wie in der letzten ausgewählten Cam nehme wieder die gleiche
                if (self.get_amount_of_people(x, last_cam)) == (self.get_amount_of_people(x, choosen_cam)):
                    choosen_cam = last_cam

            # überschreibe last_cam_amunt und last_cam
            last_cam_amount = self.__frames[x].get_camera_amount()
            last_cam = choosen_cam

            print("Frame : ", x, " choosencam : ", choosen_cam)

            # ungefiltertes Ergebnis-Array
            result_arr.append((choosen_cam, x))

        if show_graph:
            # Grapherstellung
            gh = GraphHelper(score_array, self.__frames)
            gh.show_algodata_graph(False, "Multiperson Score Curve")

        return result_arr

    def run_multiperson_close_up(self, show_graph):
        result_arr = []
        choosen_cam = 0
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
