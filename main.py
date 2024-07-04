import pyaudio
import wave
import speech_recognition as sr

def record_audio(filename, duration):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    p = pyaudio.PyAudio()

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []

    for i in range(0, int(fs / chunk * duration)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    print('Finished recording')

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio(filename):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(filename)

    with audio_file as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

def main():
    audio_filename = 'output.wav'
    text_filename = 'output.txt'
    duration = 10  # Duration of recording in seconds

    record_audio(audio_filename, duration)
    text = transcribe_audio(audio_filename)

    if text:
        with open(text_filename, 'w') as f:
            f.write(text)
        print(f'Transcription saved to {text_filename}')
    else:
        print('No transcription available.')

if __name__ == '__main__':
    main()

