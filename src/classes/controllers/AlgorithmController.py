from src.classes.controllers.DistanceDectionController import DistanceDetectionController
from src.classes.core.Base import Base
from src.classes.controllers.PoseController import PoseController
from src.classes.controllers.MultiPersonController import MultiPersonController


class AlgorithmController(Base):
    def __init__(self, controller):
        self.__frameData = controller.frames
        self.__frameCount = len(self.__frameData)
        self.__threshold = 26

    # Starte analyse
    def run_algorithm(self, algo_id, show_graph):
        if algo_id == 0:
            pc = PoseController(self.__frameData)
            return self.filter_cut_frames(pc.run_pose_algorithm(show_graph))
        elif algo_id == 1:
            dc = DistanceDetectionController(self.__frameData)
            return self.filter_cut_frames(dc.run_distance_algorithm(show_graph))
        elif algo_id == 2:
            mpc1 = MultiPersonController(self.__frameData)
            return self.filter_cut_frames(mpc1.run_multiperson_algorithm(0, show_graph))
        elif algo_id == 3:
            mpc2 = MultiPersonController(self.__frameData)
            return self.filter_cut_frames(mpc2.run_multiperson_algorithm(1, show_graph))
        else:
            print("Invalid algorithm ID !")
            return None

    # Extrahiert die Frames an denen das Video gecuttet wird
    def filter_cut_frames(self, switch_frames):
        cut_frames = []
        previous_cam = -1
        last_switch_frame = 0

        # Iteriere all frames
        for x in range(0, len(switch_frames)):
            # Vergleiche aktuelle cam mit vorheriger cam
            if switch_frames[x][0] != previous_cam:
                # treshhold um zu schnelle switches rauszufiltern
                if x <= last_switch_frame + self.__threshold:
                    continue

                last_switch_frame = x

                # Ueberschreibe vorherige Cam
                previous_cam = switch_frames[x][0]
                # Adde switch frames im array
                cut_frames.append((previous_cam, switch_frames[x][1]))
                # Debug output
                print("[Data] : Switch on cam ", previous_cam, "frame ", switch_frames[x][1])

        return cut_frames
