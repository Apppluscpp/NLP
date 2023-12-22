from flask import Flask, render_template, request, jsonify
import speech_recognition as sr

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/speech', methods=['POST'])
def process_speech():
    if 'audio' in request.files:
        audio_file = request.files['audio']
        recognizer = sr.Recognizer()

        with sr.AudioFile(audio_file) as source:
            audio_data = recognizer.record(source)

        try:
            text = recognizer.recognize_google(audio_data)
            return jsonify({'text': text})
        except sr.UnknownValueError:
            return jsonify({'text': 'Speech not recognized'})

    return jsonify({'error': 'No audio file provided'})

if __name__ == '__main__':
    app.run(debug=True)
