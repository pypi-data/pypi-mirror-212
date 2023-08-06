import tensorflow as tf
import pkg_resources
import numpy as np
import math
import cv2
import mediapipe as mp
import matplotlib.pyplot as plt

resource_path = 'models/lstm_model_pushup.h5'
filename = pkg_resources.resource_filename(__name__, resource_path)
pushup_model = tf.keras.models.load_model(filename)

resource_path = 'models/lstm_model_situp.h5'
filename = pkg_resources.resource_filename(__name__, resource_path)
situp_model = tf.keras.models.load_model(filename)

resource_path = 'models/lstm_model_squat.h5'
filename = pkg_resources.resource_filename(__name__, resource_path)
squat_model = tf.keras.models.load_model(filename)


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


def get_angle(a, b, c):
    # Calculate vectors
    ba = np.array([a.x - b.x, a.y - b.y])
    bc = np.array([c.x - b.x, c.y - b.y])

    # Calculate dot product
    dot_product = np.dot(ba, bc)

    # Calculate magnitudes
    magnitude_ba = np.linalg.norm(ba)
    magnitude_bc = np.linalg.norm(bc)

    # Calculate cosine of angle
    cosine_angle = dot_product / (magnitude_ba * magnitude_bc)

    # Calculate angle in radians and degrees
    angle_rad = math.acos(cosine_angle)
    angle_deg = math.degrees(angle_rad)

    return angle_deg


def get_distance(a, b):
    p_a = np.array([a.x, a.y])
    p_b = np.array([b.x, b.y])

    # print(p_a, p_b)

    distance = np.linalg.norm(p_b - p_a)

    # print(distance)

    return distance


HAND_ANGLE_LOWER_THRESHOLD = 30
HAND_ANGLE_UPPER_THRESHOLD = 110
DISTANCE_THRESHOLD = 0.29


def get_left_hand_angle(result):
    left_angle = 180

    try:
        left_shoulder = result.pose_landmarks.landmark[get_index("left_shoulder")]
        left_elbow = result.pose_landmarks.landmark[get_index("left_elbow")]
        left_wrist = result.pose_landmarks.landmark[get_index("left_wrist")]
        left_angle = get_angle(left_shoulder, left_elbow, left_wrist)
    except:
        pass

    return left_angle


def get_right_hand_angle(result):
    right_angle = 180

    try:
        right_shoulder = result.pose_landmarks.landmark[get_index("right_shoulder")]
        right_elbow = result.pose_landmarks.landmark[get_index("right_elbow")]
        right_wrist = result.pose_landmarks.landmark[get_index("right_wrist")]
        right_angle = get_angle(right_shoulder, right_elbow, right_wrist)
    except:
        pass

    return right_angle


def check_pushup_distance(result):
    nose = 100
    left_wrist = 100
    right_wrist = 100
    distance = 500

    try:
        nose = result.pose_landmarks.landmark[get_index("nose")]
        left_wrist = result.pose_landmarks.landmark[get_index("left_wrist")]
        right_wrist = result.pose_landmarks.landmark[get_index("right_wrist")]

        distance_1 = get_distance(nose, left_wrist)
        distance_2 = get_distance(nose, right_wrist)
        distance = (distance_1 + distance_2) / 2
    except:
        pass

    return distance


def count_pushup(result):
    # Getting necessary points that can be used for push ups
    left_angle = 0
    right_angle = 0

    try:
        left_hand_angle = get_left_hand_angle(result)
        right_hand_angle = get_right_hand_angle(result)
        distance = check_pushup_distance(result)
    except:
        pass

    return {
        "status": (HAND_ANGLE_LOWER_THRESHOLD < left_hand_angle < HAND_ANGLE_UPPER_THRESHOLD and
                   HAND_ANGLE_LOWER_THRESHOLD < right_hand_angle < HAND_ANGLE_UPPER_THRESHOLD),
        "is_down": distance < DISTANCE_THRESHOLD,
        'left angle': left_hand_angle,
        'right angle': right_hand_angle,
    }


def push_up(result, img, last_status, counter):
    try:
        result_obj = count_pushup(result)
        left_angle = result_obj['left angle']
        right_angle = result_obj['right angle']
        status = result_obj['status']
        is_down = result_obj['is_down']
        distance = check_pushup_distance(result)

        if (status is (not last_status['pushup'])) and status and is_down:
            counter['pushup'] += 1

        last_status['pushup'] = status

        cv2.putText(img, f'{left_angle=}',
                    (0, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), thickness=2)
        cv2.putText(img, f'{right_angle=}',
                    (0, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), thickness=2)
        cv2.putText(img, f'{counter["pushup"]=}',
                    (0, 150),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), thickness=2)
        cv2.putText(img, f'{status=}',
                    (0, 200),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), thickness=2)
        cv2.putText(img, f'{distance=}',
                    (0, 250),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), thickness=2)
        cv2.putText(img, f'{is_down=}',
                    (0, 300),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 255, 0), thickness=2)

    except:
        pass


FOOT_LOWER_THRESHOLD = 20
FOOT_UPPER_THRESHOLD = 100
BODY_LOWER_THRESHOLD = 20
BODY_UPPER_THRESHOLD = 90
SITUP_DISTANCE_THRESHOLD = 0.2


def check_situp_distance():
    right_shoulder = 100
    right_knee = 100
    left_shoulder = 100
    left_knee = 100
    distance = 500

    try:
        right_shoulder = result.pose_landmarks.landmark[get_index("right_shoulder")]
        right_knee = result.pose_landmarks.landmark[get_index("right_knee")]
        distance_1 = get_distance(right_shoulder, right_knee)

        left_shoulder = result.pose_landmarks.landmark[get_index("left_shoulder")]
        left_knee = result.pose_landmarks.landmark[get_index("left_knee")]
        distance_2 = get_distance(left_shoulder, left_knee)

        distance = (distance_1 + distance_2) / 2

    except:
        pass

    return distance


def get_left_foot_angle(result):
    left_foot_angle = 180

    try:
        left_hip = result.pose_landmarks.landmark[get_index("left_hip")]
        left_knee = result.pose_landmarks.landmark[get_index("left_knee")]
        left_ankle = result.pose_landmarks.landmark[get_index("left_ankle")]

        left_foot_angle = get_angle(left_hip, left_knee, left_ankle)
    except:
        pass

    return left_foot_angle


def get_right_foot_angle(result):
    right_foot_angle = 180

    try:
        right_hip = result.pose_landmarks.landmark[get_index("right_hip")]
        right_knee = result.pose_landmarks.landmark[get_index("right_knee")]
        right_ankle = result.pose_landmarks.landmark[get_index("right_ankle")]

        right_foot_angle = get_angle(right_hip, right_knee, right_ankle)
    except:
        pass

    return right_foot_angle


def get_right_body_angle(result):
    body_angle = 180

    try:
        right_shoulder = result.pose_landmarks.landmark[get_index("right_shoulder")]
        right_hip = result.pose_landmarks.landmark[get_index("right_hip")]
        right_knee = result.pose_landmarks.landmark[get_index("right_knee")]

        body_angle = get_angle(right_shoulder, right_hip, right_knee)
    except:
        pass

    return body_angle


def get_left_body_angle(result):
    body_angle = 180

    try:
        left_shoulder = result.pose_landmarks.landmark[get_index("left_shoulder")]
        left_hip = result.pose_landmarks.landmark[get_index("left_hip")]
        left_knee = result.pose_landmarks.landmark[get_index("left_knee")]

        body_angle = get_angle(left_shoulder, left_hip, left_knee)
    except:
        pass

    return body_angle


def count_situp(result):
    left_foot_angle = 0
    right_foot_angle = 0
    left_body_angle = 0
    right_body_angle = 0
    distance = 0

    try:
        left_foot_angle = get_left_foot_angle(result)
        right_foot_angle = get_right_foot_angle(result)
        left_body_angle = get_left_body_angle(result)
        right_body_angle = get_right_body_angle(result)
        distance = check_situp_distance()

        # print(distance)
    except:
        print("not found")

    return {
        'left_foot_angle': left_foot_angle,
        'right_foot_angle': right_foot_angle,
        'left_body_angle': left_body_angle,
        'right_body_angle': right_body_angle,
        'distance': distance,
        'status': FOOT_LOWER_THRESHOLD < left_foot_angle < FOOT_UPPER_THRESHOLD and
                  FOOT_LOWER_THRESHOLD < right_foot_angle < FOOT_UPPER_THRESHOLD and
                  BODY_LOWER_THRESHOLD < left_body_angle < BODY_UPPER_THRESHOLD and
                  BODY_LOWER_THRESHOLD < right_body_angle < BODY_UPPER_THRESHOLD and
                  distance < SITUP_DISTANCE_THRESHOLD
    }


xd = []


def sit_up(result, img, last_status, counter):
    result_obj = count_situp(result)

    # print(result_obj['status'])

    if len(xd) == 0:
        xd.append(result_obj['status'])
    else:
        if xd[len(xd) - 1] and not (result_obj['status']):
            xd.append(result_obj['status'])
        if not xd[len(xd) - 1] and (result_obj['status']):
            xd.append(result_obj['status'])

    print(xd)

    counter['situp'] = 0
    for i in xd:
        if i:
            counter['situp'] += 1

    left_angle = result_obj['left_foot_angle']
    right_angle = result_obj['right_foot_angle']
    left_body_angle = result_obj['left_body_angle']
    right_body_angle = result_obj['right_body_angle']
    is_down = left_body_angle > 90 and right_body_angle > 90
    status = result_obj['status']

    left_angle_color = (0, 255, 0) if FOOT_LOWER_THRESHOLD < left_angle < FOOT_UPPER_THRESHOLD else (255, 0, 0)
    right_angle_color = (0, 255, 0) if FOOT_LOWER_THRESHOLD < right_angle < FOOT_UPPER_THRESHOLD else (255, 0, 0)
    left_body_color = (0, 255, 0) if BODY_LOWER_THRESHOLD < left_body_angle < BODY_UPPER_THRESHOLD else (255, 0, 0)
    right_body_color = (0, 255, 0) if BODY_LOWER_THRESHOLD < right_body_angle < BODY_UPPER_THRESHOLD else (255, 0, 0)

    cv2.putText(img, f'{left_angle=}',
                (0, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                left_angle_color, thickness=2)
    cv2.putText(img, f'{right_angle=}',
                (0, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                right_angle_color, thickness=2)
    cv2.putText(img, f'{left_body_angle=}',
                (0, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                left_body_color, thickness=2)
    cv2.putText(img, f'{right_body_angle=}',
                (0, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                right_body_color, thickness=2)
    cv2.putText(img, f'{status=}',
                (0, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), thickness=2)
    cv2.putText(img, f'{is_down=}',
                (0, 300),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), thickness=2)
    cv2.putText(img, f'{counter["situp"]=}',
                (0, 350),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), thickness=2)


SQUAT_FOOT_LOWER_THRESHOLD = 30
SQUAT_FOOT_UPPER_THRESHOLD = 90
SQUAT_DISTANCE_THRESHOLD = 0.11


def count_squat(result):
    left_foot_angle = 180
    right_foot_angle = 180
    distance = 0

    # todo
    #  get the angle from the hip to feet
    try:
        left_foot_angle = get_left_foot_angle(result)
        right_foot_angle = get_right_foot_angle(result)
        left_hip = result.pose_landmarks.landmark[get_index("left_hip")]
        left_ankle = result.pose_landmarks.landmark[get_index("left_ankle")]

        right_hip = result.pose_landmarks.landmark[get_index("right_hip")]
        right_ankle = result.pose_landmarks.landmark[get_index("right_ankle")]

        distance = (get_distance(left_hip, left_ankle) + get_distance(right_hip, right_ankle)) / 2
    except:
        pass

    # todo
    #  return an object that contains the status, the angle, and the distance
    return {
        'left_foot_angle': left_foot_angle,
        'right_foot_angle': right_foot_angle,
        'distance': distance,
        'status': SQUAT_FOOT_LOWER_THRESHOLD < left_foot_angle < SQUAT_FOOT_UPPER_THRESHOLD and
                  SQUAT_FOOT_LOWER_THRESHOLD < right_foot_angle < SQUAT_FOOT_UPPER_THRESHOLD and
                  distance < SQUAT_DISTANCE_THRESHOLD
    }


def squat(result, img, last_status, counter):
    # todo
    #  get all the data from count_squat
    result_obj = count_squat(result)
    left_angle = result_obj['left_foot_angle']
    right_angle = result_obj['right_foot_angle']
    distance = result_obj['distance']
    status = result_obj['status']

    # todo
    #  create color specific correction for all the data
    left_angle_color = (0, 255, 0) if SQUAT_FOOT_LOWER_THRESHOLD < left_angle < SQUAT_FOOT_UPPER_THRESHOLD else (
        255, 0, 0)
    right_angle_color = (0, 255, 0) if SQUAT_FOOT_LOWER_THRESHOLD < right_angle < SQUAT_FOOT_UPPER_THRESHOLD else (
        255, 0, 0)

    if (status == (not last_status['squat'])) and status:
        counter['squat'] += 1

    last_status['squat'] = status

    # todo
    #  put text for all the data in the screen
    cv2.putText(img, f'{left_angle=}',
                (0, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                left_angle_color, thickness=2)
    cv2.putText(img, f'{right_angle=}',
                (0, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                right_angle_color, thickness=2)
    cv2.putText(img, f'{status=}',
                (0, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), thickness=2)
    cv2.putText(img, f'{counter["squat"]=}',
                (0, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), thickness=2)
    cv2.putText(img, f'{distance=}',
                (0, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), thickness=2)
    cv2.putText(img, f'{last_status["squat"]}',
                (0, 300),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 0), thickness=2)


from keras.applications import ResNet50

base_model = ResNet50(weights='imagenet',
                      include_top=False,
                      pooling='avg',
                      input_shape=(224, 224, 3))


def extract_features(video_clips):
    features = []
    for clip in video_clips:
        # Preprocess the video clip
        preprocessed_clip = tf.keras.applications.resnet50.preprocess_input(clip)
        preprocessed_clip = (np.expand_dims(preprocessed_clip, axis=0))
        # Extract features using the pre-trained CNN
        features.append(base_model.predict(preprocessed_clip, verbose=0))
    return np.array(features)


mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.3,
                    model_complexity=2, enable_segmentation=True)
mp_drawing = mp.solutions.drawing_utils

from google.colab.patches import cv2_imshow

img_size = 224


def count_accuracy_pushup(video, max_frames=30, resize=(img_size, img_size)):
    frames = []

    for frame in video:
        frame = cv2.resize(frame, resize)
        frame = frame[:, :, [2, 1, 0]]
        frames.append(frame)

        if len(frames) == max_frames:
            break

    frames = np.array(frames)

    extracted_features = extract_features(frames)

    predicted = pushup_model.predict(np.expand_dims(extracted_features, axis=1), verbose=0)

    average = np.average(predicted)
    print("pushup accuracy : ")
    print(average * 100)

    return average


def count_accuracy_situp(video, max_frames=30, resize=(img_size, img_size)):
    frames = []

    for frame in video:
        frame = cv2.resize(frame, resize)
        frame = frame[:, :, [2, 1, 0]]
        frames.append(frame)

        if len(frames) == max_frames:
            break

    frames = np.array(frames)

    extracted_features = extract_features(frames)

    predicted = situp_model.predict(np.expand_dims(extracted_features, axis=1), verbose=0)

    average = np.average(predicted)
    print("situp accuracy : ")
    print(average * 100)

    return average


def count_accuracy_squat(video, max_frames=30, resize=(img_size, img_size)):
    frames = []

    for frame in video:
        frame = cv2.resize(frame, resize)
        frame = frame[:, :, [2, 1, 0]]
        frames.append(frame)

        if len(frames) == max_frames:
            break

    frames = np.array(frames)

    extracted_features = extract_features(frames)

    predicted = squat_model.predict(np.expand_dims(extracted_features, axis=1), verbose=0)

    average = np.average(predicted)
    print("squat accuracy : ")
    print(average * 100)

    return average


def check_move(move, video_path):
    detected_move = {
        'pushup': 'pushup' == str.lower(move),
        'situp': 'situp' == str.lower(move),
        'squat': 'squat' == str.lower(move),
    }

    counter = {
        'pushup': 0,
        'situp': 0,
        'squat': 0,
    }

    last_status = {
        'pushup': False,
        'situp': False,
        'squat': False,
    }

    accuracy = {
        'pushup': [],
        'situp': [],
        'squat': [],
    }

    cap = cv2.VideoCapture(video_path)
    move_arr = []

    random_poses = []
    random_poses_updated = []

    while True:
        # Read camera input
        success, img = cap.read()

        if not success:
            break

        height, width = img.shape[:2]

        # Detect pose landmarks
        clean_img = img.copy()
        random_poses.append(clean_img)
        random_poses_updated.append(img)

        move_arr.append(clean_img)

        if len(move_arr) == 30:
            if detected_move['pushup']:
                pushup_acc = count_accuracy_pushup(move_arr)
                accuracy['pushup'].append(pushup_acc)

            if detected_move['situp']:
                situp_acc = count_accuracy_situp(move_arr)
                accuracy['situp'].append(situp_acc)

            if detected_move['squat']:
                squat_acc = count_accuracy_squat(move_arr)
                accuracy['squat'].append(squat_acc)

            move_arr = []

        result = pose.process(img)

        if detected_move['pushup']:
            push_up(result, img, last_status, counter)
        if detected_move['situp']:
            sit_up(result, img, last_status, counter)
        if detected_move['squat']:
            squat(result, img, last_status, counter)



        # Draw landmarks on the image
        if result.pose_landmarks:
            mp_drawing.draw_landmarks(image=img, landmark_list=result.pose_landmarks,
                                      connections=mp_pose.POSE_CONNECTIONS)

        # if detected_move['situp']:
        #     sit_up(result, last_status, counter)

        # if detected_move['squat']:
        #     squat(result, last_status, counter)

        # Display image
        # cv2.imshow("Image", img)
        # print(len(pushup_split))

        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break

    # Release resources
    cap.release()

    plt.title('Test Pushup')
    random_images = [random_poses[15], random_poses_updated[15]]
    for num, img in enumerate(random_images):
        plt.subplot(1, len(random_images), num + 1)
        plt.axis('off')
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    print('--- done processing video ---')
    print("--- counting accuracy ---")

    if np.average(np.array(accuracy["pushup"])) * 100 < 88:
        counter['pushup'] = 0
    if np.average(np.array(accuracy["situp"])) * 100 < 88:
        counter['situp'] = 0
    if np.average(np.array(accuracy["squat"])) * 100 < 88:
        counter['squat'] = 0

    if detected_move['pushup']:
        print(
            f'--- PUSHUP ACCURACY AND COUNT --- \n Accuracy : {np.average(np.array(accuracy["pushup"])) * 100} \n Count : {counter["pushup"]} reps')

    if detected_move['situp']:
        print(
            f'--- SITUP ACCURACY AND COUNT --- \n Accuracy : {np.average(np.array(accuracy["situp"])) * 100} \n Count : {counter["situp"]} reps')

    if detected_move['squat']:
        print(
            f'--- SQUAT ACCURACY AND COUNT --- \n Accuracy : {np.average(np.array(accuracy["squat"])) * 100} \n Count : {counter["squat"]} reps')
