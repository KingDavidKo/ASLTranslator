from flask import Flask, render_template, request

app = Flask(__name__)

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
    # Perform processing logic here
    # Example: Separate the message into lists
    asl_lists = message.split(' ')
    return asl_lists

if __name__ == '__main__':
    app.run()

