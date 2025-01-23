import cv2
import argparse
from utils import *
import mediapipe as mp
from body_part_angle import BodyPartAngle
from types_of_exercise import TypeOfExercise
import mediapipe
import math
import subprocess

# Function to display the menu and get user input
def display_menu():
    print("Select the exercise type:")
    print("1. Sit-up")
    print("2. Pull-up")
    print("3. Push-up")
    print("4. Squat")
    print("5. Walk")
    print("6. Jumping Jack")  # Added Jumping Jack option
    exercise_map = {
        "1": "sit-up",
        "2": "pull-up",
        "3": "push-up",
        "4": "squat",
        "5": "walk",
        "6": "jumping-jack"  # Map option 6 to "jumping-jack"
    }
    choice = input("Enter the number of your choice: ")
    return exercise_map.get(choice, None)
# Mediapipe setup
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Display menu and get user's choice
exercise_type = display_menu()
if exercise_type is None:
    print("Invalid choice! Exiting...")
    exit()


if exercise_type == "jumping-jack":
    subprocess.run(["python", "C:\\Users\\Debarghya Kundu\\AI-Fitness-trainer\\jump.py"])
    exit()

# Start video capture
video_source = input("Enter video file name (leave empty to use webcam): ")
if video_source.strip():
    cap = cv2.VideoCapture("Exercise Videos/" + video_source)
else:
    cap = cv2.VideoCapture(0)  # webcam

cap.set(3, 800)  # width
cap.set(4, 480)  # height

# Start Mediapipe Pose detection
with mp_pose.Pose(min_detection_confidence=0.5,
                  min_tracking_confidence=0.5) as pose:

    counter = 0  # movement of exercise
    status = True  # state of move
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Failed to read video feed. Exiting...")
            break

        frame = cv2.resize(frame, (800, 480), interpolation=cv2.INTER_AREA)
        # Recolor frame to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame.flags.writeable = False
        # Make detection
        results = pose.process(frame)
        # Recolor back to BGR
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        try:
            landmarks = results.pose_landmarks.landmark
            # Updated to handle all exercises, excluding jumping-jack
            counter, status = TypeOfExercise(landmarks).calculate_exercise(
                exercise_type, counter, status)
        except:
            pass

        # Render score table with the updated exercise type
        frame = score_table(exercise_type, frame, counter, status)

        # Render detections (for landmarks)
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(255, 255, 255),
                                   thickness=2,
                                   circle_radius=2),
            mp_drawing.DrawingSpec(color=(174, 139, 45),
                                   thickness=2,
                                   circle_radius=2),
        )

        cv2.imshow('Video', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
