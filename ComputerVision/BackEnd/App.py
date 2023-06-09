from flask import Flask, render_template, request

app = Flask(__name__)

asl_mapping = {
    'A': 'ComputerVision/BackEnd/static/asl.alpha.images/A.jpg',
    'B': 'ComputerVision/BackEnd/static/asl.alpha.images/B.jpg',
    'C': 'ComputerVision/BackEnd/static/asl.alpha.images/C.jpg',
    'D': 'ComputerVision/BackEnd/static/asl.alpha.images/D.jpg',
    'E': 'ComputerVision/BackEnd/static/asl.alpha.images/E.jpg',
    'F': 'ComputerVision/BackEnd/static/asl.alpha.images/F.jpg',
    'G': 'ComputerVision/BackEnd/static/asl.alpha.images/G.jpg',
    'H': 'ComputerVision/BackEnd/static/asl.alpha.images/H.jpg',
    'I': 'ComputerVision/BackEnd/static/asl.alpha.images/I.jpg',
    'J': 'ComputerVision/BackEnd/static/asl.alpha.images/J.jpg',
    'K': 'ComputerVision/BackEnd/static/asl.alpha.images/K.jpg',
    'L': 'ComputerVision/BackEnd/static/asl.alpha.images/L.jpg',
    'M': 'ComputerVision/BackEnd/static/asl.alpha.images/M.jpg',
    'N': 'ComputerVision/BackEnd/static/asl.alpha.images/N.jpg',
    'O': 'ComputerVision/BackEnd/static/asl.alpha.images/O.jpg',
    'P': 'ComputerVision/BackEnd/static/asl.alpha.images/P.jpg',
    'Q': 'ComputerVision/BackEnd/static/asl.alpha.images/Q.jpg',
    'R': 'ComputerVision/BackEnd/static/asl.alpha.images/R.jpg',
    'S': 'ComputerVision/BackEnd/static/asl.alpha.images/S.jpg',
    'T': 'ComputerVision/BackEnd/static/asl.alpha.images/T.jpg',
    'U': 'ComputerVision/BackEnd/static/asl.alpha.images/U.jpg',
    'V': 'ComputerVision/BackEnd/static/asl.alpha.images/V.jpg',
    'W': 'ComputerVision/BackEnd/static/asl.alpha.images/W.jpg',
    'X': 'ComputerVision/BackEnd/static/asl.alpha.images/X.jpg',
    'Y': 'ComputerVision/BackEnd/static/asl.alpha.images/Y.jpg',
    'Z': 'ComputerVision/BackEnd/static/asl.alpha.images/Z.jpg',
}



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/text_to_asl', methods=['GET', 'POST'])
def text_to_asl():
    if request.method == 'POST':
        message = request.form['message']
        asl_lists = textToList(message)
        return render_template('text_to_asl.html', asl_lists=asl_lists)

    return render_template('text_to_asl.html')

@app.route('/asl_to_text')
def asl_to_text():
    return render_template('asl_to_text.html')

def textToList(message):
    translated_images = []
    for word in message.split():
        asl_images = [asl_mapping.get(letter.upper()) for letter in word]
        translated_images.extend(asl_images)
    return translated_images

if __name__ == '__main__':
    app.run()

