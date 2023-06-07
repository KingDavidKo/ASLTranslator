from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/text_to_asl')
def text_to_asl():
    return render_template('text_to_asl.html')

@app.route('/asl_to_text')
def asl_to_text():
    return render_template('asl_to_text.html')

if __name__ == '__main__':
    app.run()
