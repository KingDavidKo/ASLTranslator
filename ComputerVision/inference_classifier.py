import pickle

import cv2
import mediapipe as mp
import numpy as np

model_dict1 = pickle.load(open('./model1.p', 'rb'))
#model_dict2 = pickle.load(open('./model2.p', 'rb'))
model1 = model_dict1['model1']
#model2 = model_dict2['model2']


cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, max_num_hands=2 ,min_detection_confidence=0.3)


labels_dict1 = {0: 'A', 1: 'B', 2: 'C',3: 'D', 4: 'E',5:'F',6: 'G', 7: 'H', 8: 'I',9: 'J', 10: 'K',11:'L',12: 'M', 13: 'N',14:'O',15: 'P', 16: 'Q', 17: 'R',18: 'S', 19: 'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z'}
while True:

    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()

    H, W, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        n = len(results.multi_hand_landmarks)
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # image to draw
                hand_landmarks,  # model output
                mp_hands.HAND_CONNECTIONS,  # hand connections
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))
        if n==1:
            
            x1 = int(min(x_) * W) - 10
            y1 = int(min(y_) * H) - 10

            x2 = int(max(x_) * W) - 10
            y2 = int(max(y_) * H) - 10

            prediction1 = model1.predict([np.asarray(data_aux)])

            predicted_character1 = labels_dict1[int(prediction1[0])]
            if x1<0 or x2>W or y1<0 or y2>H:
                cv2.putText(frame, 'Keep Hand On Screen', (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0, 255), 3,
                    cv2.LINE_AA)
            elif (x2-x1)*(y2-y1)/(W*H) <0.05:
                cv2.putText(frame, 'Move Forward', (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3,
                    cv2.LINE_AA)
                
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
            cv2.putText(frame, predicted_character1, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3,
                        cv2.LINE_AA)

                
        else:
            cv2.putText(frame, 'One Hand Only Please', (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2,
                    cv2.LINE_AA)
            
    if cv2.waitKey(25) == ord('q'):
        break
    cv2.putText(frame, 'Press Q to exit', (W-175, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2,
                    cv2.LINE_AA)
    cv2.imshow('frame', frame)
    cv2.waitKey(1)


cap.release()
cv2.destroyAllWindows()