import cv2
import mediapipe as mp
from collections import deque

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def get_finger_states(hand_landmarks):
    tips = [4, 8, 12, 16, 20]
    pip = [3, 6, 10, 14, 18]

    fingers = []

    # Polegar (eixo X)
    fingers.append(
        hand_landmarks.landmark[tips[0]].x >
        hand_landmarks.landmark[pip[0]].x
    )

    # Outros dedos (eixo Y)
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

gesture_history = deque(maxlen=5)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
) as hands:

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        gesture = "Nenhum"

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                fingers = get_finger_states(hand_landmarks)
                current_gesture = classify_gesture(fingers)

                gesture_history.append(current_gesture)

                gesture = max(
                    set(gesture_history),
                    key=gesture_history.count
                )

        cv2.putText(
            frame,
            gesture,
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow("Gesture Classification", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()

