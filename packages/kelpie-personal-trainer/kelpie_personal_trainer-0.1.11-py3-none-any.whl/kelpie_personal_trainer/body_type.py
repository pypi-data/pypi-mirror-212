import pickle
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import pkg_resources

resource_path = 'models\knnpickle_file.pickle'
filename = pkg_resources.resource_filename(__name__, resource_path)

model = pickle.load(open(filename, 'rb'))


def get_index(name):
    landmark_names = [
        'nose',
        'left_eye_inner', 'left_eye', 'left_eye_outer',
        'right_eye_inner', 'right_eye', 'right_eye_outer',
        'left_ear', 'right_ear',
        'mouth_left', 'mouth_right',
        'left_shoulder', 'right_shoulder',
        'left_elbow', 'right_elbow',
        'left_wrist', 'right_wrist',
        'left_pinky_1', 'right_pinky_1',
        'left_index_1', 'right_index_1',
        'left_thumb_2', 'right_thumb_2',
        'left_hip', 'right_hip',
        'left_knee', 'right_knee',
        'left_ankle', 'right_ankle',
        'left_heel', 'right_heel',
        'left_foot_index', 'right_foot_index',
    ]
    return landmark_names.index(name)


def get_distance(a, b):
    p_a = np.array([a.x, a.y])
    p_b = np.array([b.x, b.y])

    # print(p_a, p_b)

    distance = np.linalg.norm(p_b - p_a)

    # print(distance)

    return distance


def get_shoulder_distance(result):
    right_shoulder = ""
    left_shoulder = ""
    try:
        right_shoulder = result.pose_landmarks.landmark[get_index("right_shoulder")]
        left_shoulder = result.pose_landmarks.landmark[get_index("left_shoulder")]
    except:
        print("finished")

    if left_shoulder is not None and right_shoulder is not None:
        return get_distance(left_shoulder, right_shoulder)


def get_waist_distance(result):
    right_hip = ""
    left_hip = ""

    try:
        right_hip = result.pose_landmarks.landmark[get_index("right_hip")]
        left_hip = result.pose_landmarks.landmark[get_index("left_hip")]
    except:
        print("finished")

    if left_hip is not None and right_hip is not None:
        return get_distance(left_hip, right_hip)

mp_pose = mp.solutions.pose

pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3,
                    model_complexity=2, enable_segmentation=True)

def check_body(path):
    img = cv2.imread(path)
    PPI = 10

    shape = img.shape[:-1]

    result = pose.process(img)

    shoulder = (get_shoulder_distance(result) * shape[1]) / PPI
    waist = (get_waist_distance(result) * shape[1]) / PPI
    ratio = shoulder / waist

    print([[shoulder, waist, ratio]])

    return model.predict(
        pd.DataFrame([[shoulder, waist, ratio]], columns=['ShoulderWidth', 'Waist ', 'shoulder-waist']))
