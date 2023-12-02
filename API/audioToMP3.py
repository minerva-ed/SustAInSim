import pyaudio
import wave
from pydub import AudioSegment
import os
import signal
import sys

import pyaudio
import wave
import threading
from pydub import AudioSegment
import os

def record_audio():
    output_filename="output.mp3"
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    WAVE_OUTPUT_FILENAME = "output.wav"

    # Initialize PyAudio and start recording
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []
    stop_event = threading.Event()

    def signal_handler(sig, frame):
        print("\nRecording stopped.")
        stop_event.set()

    # Set signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    print("Recording...")

    # Continue recording until stop event is set
    while not stop_event.is_set():
        data = stream.read(CHUNK)
        frames.append(data)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as a WAV file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    # Convert to MP3
    #AudioSegment.from_wav(WAVE_OUTPUT_FILENAME).export(output_filename, format="mp3")
    #os.remove(WAVE_OUTPUT_FILENAME)

    print(f"File saved: {output_filename}")
    return WAVE_OUTPUT_FILENAME
