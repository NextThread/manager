import pyaudio
import wave
import whisper
import certifi
import ssl
import urllib.request

def record_audio(filename, duration):
    chunk = 102
    sample_format = pyaudio.paInt16
    channels = 1
    fs = 44100 
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

def transcribe_audio_with_whisper(filename):
    context = ssl.create_default_context(cafile=certifi.where()) # ssl certi issue fix/ bypass

    def patched_urlopen(*args, **kwargs):
        kwargs['context'] = context
        return original_urlopen(*args, **kwargs)
    
    original_urlopen = urllib.request.urlopen
    urllib.request.urlopen = patched_urlopen

    model = whisper.load_model("base")
    result = model.transcribe(filename)
    return result["text"]

def main():
    audio_filename = 'output.wav'
    text_filename = 'conversation.txt'
    duration = 20 #fix it later, meeting duration

    record_audio(audio_filename, duration)
    text = transcribe_audio_with_whisper(audio_filename)

    with open(text_filename, 'w') as f:
        f.write(text)

    print(f'save donee {text_filename}')

if __name__ == '__main__':
    main()
