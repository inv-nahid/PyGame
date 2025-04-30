import mediapipe as mp
import cv2
import numpy as np
import random
import time
from mediapipe.framework.formats import landmark_pb2

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

score = 0
x_enemy = random.randint(50, 600)
y_enemy = random.randint(50, 400)
enemy_visible = True  # Enemy visibility flag

def enemy(image):
    cv2.circle(image, (x_enemy, y_enemy), 25, (0, 200, 0), 5)

video = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while video.isOpened():
        _, frame = video.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        imageHeight, imageWidth, _ = image.shape

        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        font = cv2.FONT_HERSHEY_SIMPLEX
        color = (255, 0, 255)
        cv2.putText(image, "Score", (480, 30), font, 1, color, 4, cv2.LINE_AA)
        cv2.putText(image, str(score), (590, 30), font, 1, color, 4, cv2.LINE_AA)

        if enemy_visible:
            enemy(image)

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2, circle_radius=4),
                    mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=2)
                )

        if results.multi_hand_landmarks:
            for handLandmarks in results.multi_hand_landmarks:
                for point in mp_hands.HandLandmark:
                    normalizedLandmark = handLandmarks.landmark[point]
                    pixel = mp_drawing._normalized_to_pixel_coordinates(
                        normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)
                    
                    if point == mp_hands.HandLandmark.INDEX_FINGER_TIP and pixel is not None:
                        try:
                            cv2.circle(image, (pixel[0], pixel[1]), 25, (0, 200, 0), 5)
                            if abs(pixel[0] - x_enemy) < 20 and abs(pixel[1] - y_enemy) < 20:
                                print("FINGER DETECTED!")
                                score += 1
                                x_enemy = random.randint(50, 600)
                                y_enemy = random.randint(50, 400)
                                enemy_visible = True  # Show new enemy next frame
                        except:
                            pass

        cv2.imshow('Hand Tracking', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
video.release()
cv2.destroyAllWindows()
