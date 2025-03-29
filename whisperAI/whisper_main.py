import pyttsx3
import sounddevice as sd
import numpy as np
import whisper
import wave
from google import genai
from google.genai import types
import keys
# Load Whisper Model (Use "tiny.en" for speed, "base.en" for better accuracy)
model = whisper.load_model("tiny.en")

# Initialize Google Gemini API
client = genai.Client(api_key=keys.load_key())
model_name = "gemini-2.0-flash"

generate_content_config = types.GenerateContentConfig(
    temperature=1,
    top_p=0.95,
    top_k=40,
    max_output_tokens=8192,
    response_mime_type="text/plain",
    system_instruction=[
        types.Part.from_text(text="You are a helpful assistant. Motivate users to do good.")
    ],
)

chat_history = []

# Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty("rate", 170)

# Audio Recording Settings
SAMPLE_RATE = 16000  # Standard for Whisper
DURATION = 30  # 30 seconds max input
FILENAME = "input.wav"

def record_audio():
    """Records audio for 30 seconds and saves it to a file."""
    print("\n🎤 Recording... Speak now (30 sec max)")
    audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype=np.int16)
    sd.wait()
    print("✅ Recording complete. Processing...")

    # Save audio as WAV file
    with wave.open(FILENAME, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())

def transcribe_audio():
    """Uses Whisper AI to transcribe recorded audio."""
    result = model.transcribe(FILENAME)
    text = result["text"].strip()
    print("You:", text)
    return text if text else None

def speak(text):
    """Speaks the AI response quickly."""
    engine.say(text)
    engine.runAndWait()

def chat():
    """Continuously listens and responds with minimal delay."""
    while True:
        record_audio()
        user_input = transcribe_audio()
        
        if not user_input:
            print("❌ No voice detected, try again.")
            continue

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("AI: Goodbye! Have a great day!")
            speak("Goodbye! Have a great day!")
            break

        # Append user input to chat history
        chat_history.append(types.Content(role="user", parts=[types.Part.from_text(text=user_input)]))

        # Generate AI response
        print("AI:", end=" ", flush=True)
        ai_response = ""
        
        for chunk in client.models.generate_content_stream(
            model=model_name, contents=chat_history, config=generate_content_config
        ):
            print(chunk.text, end="", flush=True)
            ai_response += chunk.text

        print("\n")
        speak(ai_response)

        # Append AI response to chat history
        chat_history.append(types.Content(role="model", parts=[types.Part.from_text(text=ai_response)]))

if __name__ == "__main__":
    chat()
