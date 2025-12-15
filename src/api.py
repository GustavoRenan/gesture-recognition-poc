import cv2
import mediapipe as mp
import numpy as np
from fastapi import FastAPI, File, UploadFile
from collections import deque

app = FastAPI()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0.7
)

gesture_history = deque(maxlen=5)

def get_finger_states(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    pip = [3, 6, 10, 14, 18]

    fingers = []

    fingers.append(
        hand_landmarks.landmark[tips[0]].x >
        hand_landmarks.landmark[pip[0]].x
    )

    for i in range(1, 5):
        fingers.append(
            hand_landmarks.landmark[tips[i]].y <
            hand_landmarks.landmark[pip[i]].y
        )

    return fingers

def classify_gesture(fingers):
    if fingers == [True, True, True, True, True]:
        return "Mao Aberta"
    if fingers == [False, False, False, False, False]:
        return "Punho Fechado"
    if fingers == [True, False, False, False, False]:
        return "Polegar Para Cima"
    return "Gesto Desconhecido"

@app.post("/gesture")
async def recognize_gesture(file: UploadFile = File(...)):
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if not results.multi_hand_landmarks:
        return {"gesture": "Nenhum"}

    fingers = get_finger_states(results.multi_hand_landmarks[0])
    gesture = classify_gesture(fingers)

    gesture_history.append(gesture)
    final_gesture = max(set(gesture_history), key=gesture_history.count)

    return {"gesture": final_gesture}
