from pprint import pprint

class FrameMetaData:

    def __init__(self):

        self.__camera = []

        self.__camera_counter = 0


    def add_camera_data(self, data):

        # Kamera Counter wird erhöht
        self.__camera_counter += 1

        # Erstellt temporäres Array für alle erkannten Personen
        persons = []

        # Durchläuft alle erkannten Personen
        for e in data["people"]:

            # Fügt den Meta Daten aus den JSON FILES die zugehörigen Körperteile hinzu.
            poseData = {
                "nose": e["pose_keypoints"][0:3],
                "neck": e["pose_keypoints"][3:6],
                "left_shoulder": e["pose_keypoints"][6:9],
                "left_elbow": e["pose_keypoints"][9:12],
                "left_wrist": e["pose_keypoints"][12:15],
                "right_shoulder": e["pose_keypoints"][15:18],
                "right_elbow": e["pose_keypoints"][18:21],
                "right_wrist": e["pose_keypoints"][21:24],
                "left_hip": e["pose_keypoints"][24:27],
                "left_knee": e["pose_keypoints"][27:30],
                "left_foot": e["pose_keypoints"][30:33],
                "right_hip": e["pose_keypoints"][33:36],
                "right_knee": e["pose_keypoints"][36:39],
                "right_foot": e["pose_keypoints"][39:42],
                "left_eye": e["pose_keypoints"][42:45],
                "left_ear": e["pose_keypoints"][45:48],
                "right_eye": e["pose_keypoints"][48:51],
                "right_ear": e["pose_keypoints"][51:54],
                "face": e["face_keypoints"]
            }

            persons.append(poseData)

        # Fügt den Personen alle "Körperteile" hinzu.
        self.__camera.append({"people": persons, "precision": 0.0})


    def get_camera(self, camera):

        # schaut, ob die gegebene Kamera noch existiert.
        if camera < len(self.__camera):

            # Gibt die Kamera zurück
            return self.__camera[camera]
        else:
            print("[Error]: Camera " + str(camera) + " doesn't exist")


    def get_camera_amount(self):
        return self.__camera_counter





