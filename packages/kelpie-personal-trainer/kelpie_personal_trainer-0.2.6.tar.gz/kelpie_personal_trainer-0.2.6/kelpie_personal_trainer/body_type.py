import pickle
import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
import sklearn
import pkg_resources


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

def check_body(path, gender='male'):
    resource_path = 'models/knnpickle_file.pickle'
    filename = pkg_resources.resource_filename(__name__, resource_path)

    model = pickle.load(open(filename, 'rb'))

    if gender == 'female':
        resource_path = 'models/knnpickle_file_woman.pickle'
        filename = pkg_resources.resource_filename(__name__, resource_path)

        model = pickle.load(open(filename, 'rb'))


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

def get_menu(body_type):
    menu_latihan = {
        # MEN'S AREA
        "I-Shape": {
            'Body Parts': {
                "Chest and Shoulder": {
                    "Push-Up": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Pike Push-Up": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Wide Push-Up": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Diamond Push-Up": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                },
                "Back": {
                    "Pull-up": {
                        "Sets": 3,
                        'Reps': 8,
                    },
                    "Australian Pull-Up": {
                        "Sets": 3,
                        "Reps": 10
                    },
                    "Superman Back Extension": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Plank Row": {
                        "Sets": 3,
                        "Reps": 10,
                    }
                },
                "Arms": {
                    "Diamond Push-Up": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Tricep Dips": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Push-Up to Side Plank": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Pike Push-Up": {
                        "Sets": 3,
                        "Reps": 10,
                    }
                },
                "Legs and Stomach": {
                    "Plank": {
                        "Sets": 3,
                        "Reps": 30,
                        "Additional Notes": "seconds"
                    },
                    "Bicycle Crunch": {
                        "Sets": 3,
                        "Reps": 10,
                        "Additional Notes": "each side"
                    },
                    "Russian Twist": {
                        "Sets": 3,
                        "Reps": 10,
                        "Additional Notes": "each side"
                    },
                    "Mountain Climbers": {
                        "Sets": 3,
                        "Reps": 10,
                        "Additional Notes": "each side"
                    }
                }
            }
        },
        "A-Shape": {
            "Body Parts": {
                "Chest and Shoulder": {
                    "Push-up": {
                        "Sets": 3,
                        "Reps": 'until failure',
                    },
                    "Pike Push-ups": {
                        "Sets": 3,
                        "Reps": 'until failure',
                    },
                    "Diamond Push-ups": {
                        "Sets": 3,
                        "Reps": 'until failure',
                    },
                    "Dips": {
                        "Sets": 3,
                        "Reps": 'until failure',
                    },
                    "Superman Pose": {
                        "Sets": 3,
                        "Reps": 10,
                        "Additional Notes": "Hold 5 second every reps"
                    }
                },
                "Back": {
                    "Pull-ups": {
                        "Sets": 3,
                        "Reps": "until failure",

                    },
                    "Chin-ups": {
                        "Sets": 3,
                        "Reps": "until failure",
                    },
                    "Pike Push-ups": {
                        "Sets": 3,
                        "Reps": "until failure",
                    },
                    "Handstand Hold": {
                        "Sets": 3,
                        "Reps": "until failure",
                        "Additional Notes": "Use wall as a helper"
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "seconds"
                    }
                },
                "Legs and stomach": {
                    "Squats": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Leg Press": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Lunges": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg",
                    },
                    "Leg Curls": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Barbell Curls": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Hammer Curls": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                },
                "Upper Body and Cardiovascular Workout": {
                    "Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure",
                    },
                    "Pull-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure",
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Jumping Jacks": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Skipping": {
                        "Reps": 10,
                        "Additional Notes": "Minutes"
                    }
                }
            }
        },
        "X-Shape": {
            "Body Parts": {
                "Upper Body and Core": {
                    "Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure",
                    },
                    "Wide Arm Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure",
                    },
                    "Pike Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure",
                    },
                    "Superman Hold": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Side Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds, Each Side",
                    },
                },
                "Lower Body and Cardio": {
                    "Squats": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Alternating Lunges": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg",
                    },
                    "Glute Bridges": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "High Knees": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Jumping Jacks": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Mountain Climbers": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },

                },
                "Upper Body and Core (2)": {
                    "Diamond Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                    },
                    "Incline Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                    },
                    "Pike Handstand Push-ups (against a wall)": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Against A Wall",
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side",
                    },
                    "Russian Twists": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side",
                    },
                    "Plank Shoulder Taps": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side",
                    },
                },
                "Lower Body and Cardio (2)": {
                    "Single-Leg Squats (Pistol Squats)": {
                        "Sets": 3,
                        "Reps": 8,
                    },
                    "Calf Raises": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Jump Squats": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Burpees": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "High Knees": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Skipping": {
                        "Sets": "-",
                        "Reps": 10,
                        "Additional Notes": "Seconds",
                    }
                }
            }
        },
        "V-Shape": {
            "Body Parts": {
                "Upper Body and Core": {
                    "Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until failure",
                    },
                    "Wide Arm Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until failure",
                    },
                    "Diamond Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until failure",
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Russian Twists": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side",
                    },
                    "Superman Hold": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                },
                "Lower Body and Cardio": {
                    "Squats": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Alternating Lunges": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg",
                    },
                    "Glute Bridges": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "High Knees": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Jumping Jacks": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Mountain Climbers": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                },
                "Upper Body and Core (2)": {
                    "Pike Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until failure",
                    },
                    "Incline Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until failure",
                    },
                    "Close Grip Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until failure",
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side",
                    },
                    "Plank Shoulder Taps": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side",
                    },
                    "Side Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Each Side",
                    },
                },
                "Upper Body and Cardio (2)": {
                    "Wide Arm Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until failure",
                    },
                    "Diamond Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until failure",
                    },
                    "Archer Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure, Each Side",
                    },
                    "Burpees": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "High Knees": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                }
            }
        },
        "T-Shape": {
            "Body Parts": {
                "Upper Body and Core": {
                    "Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure",
                    },
                    "Wide Arm Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure",
                    },
                    "Pike Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure",
                    },
                    "Superman Hold": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side",
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                },
                "Lower Body and Cardio": {
                    "Squats": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Alternating Lunges": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg",
                    },
                    "Glute Bridges": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "High Knees": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Jumping Jacks": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Mountain Climbers": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                },
                "Upper Body and Core (2)": {
                    "Pike Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure",
                    },
                    "Incline Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure",
                    },
                    "Diamond Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure",
                    },
                    "Russian Twists": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Seconds, Each Side",
                    },
                    "Plank Shoulder Taps": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Seconds, Each Side",
                    },
                    "Side Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds, Each Side",
                    },
                },
                "Upper Body and Cardio": {
                    "Pull-ups (or modified version like bodyweight rows or doorframe rows)": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure",
                    },
                    "Wide Arm Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure",
                    },
                    "Dips (using a chair or bench)": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure",
                    },
                    "Burpees": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "High Knees": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                }
            }
        },
        "O-Shape": {
            "Body Parts": {
                "Cardio and Core": {
                    "Jumping Jacks": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "High Knees": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Mountain Climbers": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side",
                    },
                    "Russian Twists": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side",
                    },
                },
                "Lower Body and Cardio": {
                    "Squats": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Alternating Lunges": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg",
                    },
                    "Glute Bridges": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "High Knees": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Jumping Jacks": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Mountain Climbers": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                },
                "Upper Body and Core": {
                    "Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure",
                    },
                    "Wide Arm Push-ups": {
                        "Sets": 3,
                        "Reps": '-',
                        "Additional Notes": "Until Failure",
                    },
                    "Plank Shoulder Taps": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side",
                    },
                    "Superman Hold": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds",
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side",
                    },
                    "Russian Twists": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side",
                    },

                },
                "Full Body Circuit": {
                    "Description": "Perform each exercise in succession with minimal rest between exercises. Rest for 1-2 minutes at the end of the circuit. Repeat the circuit for a total of 3 sets.",
                    "Workout": {
                        "Jumping Jacks": {
                            "Sets": 3,
                            "Reps": 30,
                            "Additional Notes": "Seconds"
                        },
                        "Squats": {
                            "Sets": 3,
                            "Reps": 30,
                        },
                        "Push-ups": {
                            "Sets": 3,
                            "Reps": 10,
                        },
                        "Plank": {
                            "Sets": 3,
                            "Reps": 30,
                            "Additional Notes": "Seconds"
                        },
                        "Alternating Lunges": {
                            "Sets": 3,
                            "Reps": 12,
                            "Additional Notes": "Each Leg"
                        },
                        "Bicycle Crunches": {
                            "Sets": 3,
                            "Reps": 12,
                            "Additional Notes": "Each Side"
                        }
                    }
                }
            }
        },

        # WOMAN'S AREA
        "Hourglass": {
            "Body Parts": {
                "Full Body Circuit": {
                    "Description": "",
                    "Workout": {
                        "Squats": {
                            "Sets": 3,
                            "Reps": 12,
                        },
                        "Push-ups": {
                            "Sets": 3,
                            "Reps": 10,
                        },
                        "Glute Bridges": {
                            "Sets": 3,
                            "Reps": 12,
                        },
                        "Plank": {
                            "Sets": 3,
                            "Reps": 60,
                            "Additional Notes": "Seconds"
                        },
                        "Bicycle Crunches": {
                            "Sets": 3,
                            "Reps": 12,
                            "Additional Notes": "Each Side"
                        },
                        "Mountain Climbers": {
                            "Sets": 3,
                            "Reps": 60,
                            "Additional Notes": "Seconds"
                        },
                    }
                },
                "Lower Body and Core": {
                    "Squats": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Alternating Lunges": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Glute Bridges": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Side Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds, Each Side"
                    },
                    "Standing Side Leg Lifts": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                },
                "Upper Body and Core": {
                    "Push-ups": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Tricep Dips (using a chair or bench)": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Plank Shoulder Taps": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                    "Superman Hold": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                    "Standing Arm Circles": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Forward And Backward"
                    },
                },
                "Cardio and Core": {
                    "Jumping Jacks": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "High Knees": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Mountain Climbers": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Russian Twists": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                }
            }
        },
        "Bottom Hourglass": {
            "Body Parts": {
                "Lower Body and Core": {
                    "Squats": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Alternating Reverse Lunges": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Glute Bridges": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Standing Side Leg Lifts": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },

                },
                "Cardio and Core": {
                    "Jumping Jacks": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "High Knees": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Mountain Climbers": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Russian Twists": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                    "Reverse Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                },
                "Lower Body and Core (2)": {
                    "Squats": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Alternating Reverse Lunges": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Glute Bridges": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Standing Side Leg Lifts": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                },
                "Cardio and Core (2)": {
                    "Jumping Jacks": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "High Knees": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Mountain Climbers": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Russian Twists": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                    "Reverse Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                }
            }
        },
        "Top Hourglass": {
            "Body Parts": {
                "Upper Body and Core": {
                    "Push-ups": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Tricep Dips (using a chair or bench)": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Side Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds, Each Side"
                    },
                    "Standing Arm Circles": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Forward And Backward"
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                },
                "Cardio and Core": {
                    "Jumping Jacks": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "High Knees": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Mountain Climbers": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Russian Twists": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                    "Reverse Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                },
                "Upper Body and Core (2)": {
                    "Push-ups": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Tricep Dips (using a chair or bench)": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Side Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds, Each Side"
                    },
                    "Standing Arm Circles": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Forward And Backward"
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },

                },
                "Cardio and Core (2)": {
                    "Jumping Jacks": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "High Knees": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Mountain Climbers": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Russian Twists": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                    "Reverse Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                }
            }
        },
        "Spoon": {
            "Body Parts": {
                "Lower Body and Core": {
                    "Squats": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Alternating Reverse Lunges": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Glute Bridges": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Standing Side Leg Lifts": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                },
                "Upper Body and Core": {
                    "Push-ups": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Tricep Dips (using a chair or bench)": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Plank Shoulder Taps": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                    "Superman Hold": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Standing Arm Circles": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Forward And Backward"
                    },
                    "Reverse Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                },
                "Lower Body and Core (2)": {
                    "Squats": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Alternating Reverse Lunges": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Glute Bridges": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Standing Side Leg Lifts": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },

                },
                "Upper Body and Core (2)": {
                    "Push-ups": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Tricep Dips (using a chair or bench)": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Plank Shoulder Taps": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                    "Superman Hold": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Standing Arm Circles": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Forward And Backward"
                    },
                    "Reverse Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                }
            }
        },
        "Triangle": {
            "Body Parts": {
                "Upper Body and Core": {
                    "Push-ups": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Tricep Dips (using a chair or bench)": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Side Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds, Each Side"
                    },
                    "Standing Arm Circles": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Forward And Backward"
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                },
                "Lower Body and Core": {
                    "Squats": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Alternating Reverse Lunges": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Glute Bridges": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Standing Side Leg Lifts": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                },
                "Upper Body and Core (2)": {
                    "Reverse Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Tricep Dips (using a chair or bench)": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Side Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds, Each Side"
                    },
                    "Standing Arm Circles": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Forward And Backward"
                    },
                },
                "Lower Body and Core (2)": {
                    "Squats": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Alternating Reverse Lunges": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Glute Bridges": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Standing Side Leg Lifts": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Reverse Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                },
            }
        },
        "Inverted Triangle": {
            "Body Parts": {
                "Lower Body and Core": {
                    "Squats": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Alternating Reverse Lunges": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Glute Bridges": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Standing Side Leg Lifts": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                },
                "Upper Body and Core": {
                    "Push-ups": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Tricep Dips (using a chair or bench)": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Plank Shoulder Taps": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                    "Superman Hold": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Standing Arm Circles": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Forward And Backward"
                    },
                    "Reverse Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                },
                "Lower Body and Core (2)": {
                    "Squats": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Alternating Reverse Lunges": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Glute Bridges": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Standing Side Leg Lifts": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                },
                "Upper Body and Core (2)": {
                    "Push-ups": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Tricep Dips (using a chair or bench)": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Plank Shoulder Taps": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                    "Superman Hold": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Standing Arm Circles": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Forward And Backward"
                    },
                    "Reverse Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                }
            }
        },
        "Rectangle": {
            "Body Parts": {
                "Full Body Workout": {
                    "Squats": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                    "Push-ups (modified or standard)": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Reverse Lunges": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Leg"
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                    "Superman Hold": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                },
                "Cardio and Core": {
                    "Jumping Jacks": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "High Knees": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Mountain Climbers": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Russian Twists": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                    "Reverse Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                },
                "Upper Body and Core": {
                    "Tricep Dips (using a chair or bench)": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Push-ups (modified or standard)": {
                        "Sets": 3,
                        "Reps": 10,
                    },
                    "Plank Shoulder Taps": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                    "Standing Arm Circles": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Forward And Backward"
                    },
                    "Bicycle Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                    "Superman Hold": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                },
                "Cardio and Core (2)": {
                    "Jumping Jacks": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "High Knees": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Mountain Climbers": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Plank": {
                        "Sets": 3,
                        "Reps": 60,
                        "Additional Notes": "Seconds"
                    },
                    "Russian Twists": {
                        "Sets": 3,
                        "Reps": 12,
                        "Additional Notes": "Each Side"
                    },
                    "Reverse Crunches": {
                        "Sets": 3,
                        "Reps": 12,
                    },
                }
            }
        },
    }

    return menu_latihan[str.title(body_type)]
