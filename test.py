import pyaudio
import wave
import whisper

def record_audio(output_filename, record_seconds, mic_index, system_audio_index):
    FORMAT = pyaudio.paInt16
    CHANNELS = 2  # Stereo
    RATE = 44100
    CHUNK = 1024

    audio = pyaudio.PyAudio()

    # Open the stream for the system audio
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=system_audio_index,
                        frames_per_buffer=CHUNK)

    # Open the stream for the microphone
    mic_stream = audio.open(format=FORMAT,
                            channels=CHANNELS,
                            rate=RATE,
                            input=True,
                            input_device_index=mic_index,
                            frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []
    mic_frames = []

    for i in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        mic_data = mic_stream.read(CHUNK)
        frames.append(data)
        mic_frames.append(mic_data)

    print("Recording finished")

    stream.stop_stream()
    stream.close()
    mic_stream.stop_stream()
    mic_stream.close()
    audio.terminate()

    # Merge both audio streams (simple concatenation)
    merged_frames = [f + m for f, m in zip(frames, mic_frames)]

    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(merged_frames))

    print(f"Saved to {output_filename}")

def transcribe_audio_whisper(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["text"]

# Replace with actual indices of your devices
mic_index = 1  # Adjust based on your actual microphone index
system_audio_index = 3  # CABLE Output (VB-Audio Virtual Cable)

output_filename = "output.wav"
record_seconds = 60  # Adjust as needed

record_audio(output_filename, record_seconds, mic_index, system_audio_index)

transcription = transcribe_audio_whisper(output_filename)

with open("transcript.txt", "w", encoding="utf-8") as file:
    file.write(transcription)

print(f"Transcription saved to transcript.txt")
