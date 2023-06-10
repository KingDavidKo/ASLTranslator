from flask import Flask, render_template, request, Response
import pickle
import os
import cv2
import mediapipe as mp
import numpy as np
import time

app=Flask(__name__)

asl_mapping = {
    'A': 'asl.alpha.images/A.jpg',
    'B': 'asl.alpha.images/B.jpg',
    'C': 'asl.alpha.images/C.jpg',
    'D': 'asl.alpha.images/D.jpg',
    'E': 'asl.alpha.images/E.png',
    'F': 'asl.alpha.images/F.jpg',
    'G': 'asl.alpha.images/G.jpg',
    'H': 'asl.alpha.images/H.jpg',
    'I': 'asl.alpha.images/I.jpg',
    'J': 'asl.alpha.images/J.jpg',
    'K': 'asl.alpha.images/K.jpg',
    'L': 'asl.alpha.images/L.jpg',
    'M': 'asl.alpha.images/M.jpg',
    'N': 'asl.alpha.images/N.jpg',
    'O': 'asl.alpha.images/O.jpg',
    'P': 'asl.alpha.images/P.jpg',
    'Q': 'asl.alpha.images/Q.jpg',
    'R': 'asl.alpha.images/R.jpg',
    'S': 'asl.alpha.images/S.jpg',
    'T': 'asl.alpha.images/T.jpg',
    'U': 'asl.alpha.images/U.jpg',
    'V': 'asl.alpha.images/V.jpg',
    'W': 'asl.alpha.images/W.jpg',
    'X': 'asl.alpha.images/X.jpg',
    'Y': 'asl.alpha.images/Y.jpg',
    'Z': 'asl.alpha.images/Z.jpg',
}

model_dict1 = pickle.load(open('./model1.p', 'rb'))
model1 = model_dict1['model1']
message1 = ''
def gen_frames():  # generate frame by frame from camera
    
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
                percentage = list(model1.predict_proba([data_aux])[0])
                percentage = max(percentage)*100
                if percentage > 80:
                    global message1
                    message1 +=predicted_character1
                    time.sleep(1)
                    
                

                if x1<0 or x2>W or y1<0 or y2>H:
                    cv2.putText(frame, 'Keep Hand On Screen', (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,0, 255), 3,
                        cv2.LINE_AA)
                elif (x2-x1)*(y2-y1)/(W*H) <0.05:
                    cv2.putText(frame, 'Move Forward', (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3,
                        cv2.LINE_AA)
                    
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                cv2.putText(frame, predicted_character1 + str(percentage), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 0), 3,
                            cv2.LINE_AA)

                    
            else:
                cv2.putText(frame, 'One Hand Only Please', (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2,
                        cv2.LINE_AA)
        #cv2.imshow('frame', frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():

    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/asl_to_text')
def asl_to_text():
    print(message1)
    message = message1
    return render_template('asl_to_text.html',message=message)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/text_to_asl', methods=['GET', 'POST'])
def text_to_asl():
    if request.method == 'POST':
        message = request.form['message']
        asl_lists = textToList(message)
        
        return render_template('text_to_asl.html', asl_lists=asl_lists)
    app = Flask(__name__, static_folder='static')
    print(app)
    return render_template('text_to_asl.html')




def textToList(message):
    translated_images = []
    for word in message.split():
        asl_images = [asl_mapping.get(letter.upper()) for letter in word]
        translated_images.extend(asl_images)
    return translated_images

if __name__ == '__main__':
    app.run()
