from flask import Blueprint, jsonify, request
import speech_recognition as sr
from app.models import Meeting
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({"message": "Welcome to AI Scrum Master API"})

@main.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(file)
    with audio_file as source:
        audio = recognizer.record(source)
    
    try:
        transcription = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return jsonify({"error": "Speech Recognition could not understand audio"})
    except sr.RequestError as e:
        return jsonify({"error": f"Could not request results from Speech Recognition service; {e}"})
    
    new_meeting = Meeting(title=file.filename, transcription=transcription)
    db.session.add(new_meeting)
    db.session.commit()

    return jsonify({"transcription": transcription})
