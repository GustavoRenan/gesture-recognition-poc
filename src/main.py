import cv2
import mediapipe as mp
import pyautogui
import math
import numpy as np

# Desativa a trava de segurança caso o mouse vá para o canto da tela
pyautogui.FAILSAFE = False

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Pega a resolução exata do seu monitor dinamicamente
screen_w, screen_h = pyautogui.size()

# Variáveis para suavização do movimento do mouse
smoothening = 5
plocX, plocY = 0, 0
clocX, clocY = 0, 0

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

        # Espelha o frame para a coordenação motora ficar natural
        frame = cv2.flip(frame, 1)
        frame_h, frame_w, _ = frame.shape
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Dedo Indicador (8) e Polegar (4)
                index_finger = hand_landmarks.landmark[8]
                thumb = hand_landmarks.landmark[4]

                x1, y1 = int(index_finger.x * frame_w), int(index_finger.y * frame_h)
                x2, y2 = int(thumb.x * frame_w), int(thumb.y * frame_h)

                # Converte pixels da câmera para a tela do PC
                screen_x = np.interp(x1, [0, frame_w], [0, screen_w])
                screen_y = np.interp(y1, [0, frame_h], [0, screen_h])

                # Suaviza o movimento
                clocX = plocX + (screen_x - plocX) / smoothening
                clocY = plocY + (screen_y - plocY) / smoothening

                pyautogui.moveTo(clocX, clocY)
                plocX, plocY = clocX, clocY

                # Clique: mede a distância entre indicador e polegar
                distance = math.hypot(x2 - x1, y2 - y1)
                
                if distance < 30:
                    cv2.circle(frame, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                    pyautogui.click()
                    cv2.waitKey(250)

        cv2.imshow("Tony Stark POC - Controle de Mouse", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
