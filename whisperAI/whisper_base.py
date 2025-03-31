import whisper
import sounddevice as sd
import numpy as np
import wave

# Record audio function
def record_audio(filename, duration, samplerate):
    print("Recording...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    print("Recording complete.")
    
    # Save to WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

# Record and save audio
filename = "recorded_audio.wav"
record_audio(filename=filename, duration=60, samplerate=16000)

# Load Whisper model and transcribe
model = whisper.load_model("tiny.en")
result = model.transcribe(filename)
print("\n\n" + result["text"])


"""
8,000 Hz (8 kHz) – Telephone-quality audio.

16,000 Hz (16 kHz) – Used in speech recognition systems.

44,100 Hz (44.1 kHz) – CD-quality, commonly used for music.

48,000 Hz (48 kHz) – Standard for video production.

96,000 Hz (96 kHz) – High-definition audio, used in professional music production.
"""