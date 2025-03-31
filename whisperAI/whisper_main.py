from flask import Flask, render_template, request, jsonify
import sounddevice as sd
import numpy as np
import whisper
import wave
from google import genai
from google.genai import types
import keys

app = Flask(__name__)

# Load Whisper Model
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
        types.Part.from_text(text="Analyze the given text and provide insights based on these 7 parameters. Each parameter must not exceed 20 words: \n" 
                             "1. MOOD: Overall emotional state (happy, sad, neutral, etc.).\n" 
                             "2. TONE: Expressed emotion (calm, aggressive, frustrated, excited, etc.).\n" 
                             "3. CRITICALITY: Urgency or seriousness (low, moderate, high).\n" 
                             "4. LOUDNESS/AGGRESSIVENESS: Voice intensity and aggression cues.\n" 
                             "5. THEMES: Key topics or subjects detected.\n" 
                             "6. KEYWORDS: Important words or phrases.\n" 
                             "7. CHANGES IN MOOD: Any noticeable emotional shifts.")
    ],
)

# Audio Recording Settings
SAMPLE_RATE = 16000  # Standard for Whisper
DURATION = 10  # Shortened for usability
FILENAME = "static/input.wav"

def record_audio():
    """Records audio for 10 seconds and saves it to a file."""
    audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype=np.int16)
    sd.wait()
    with wave.open(FILENAME, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data.tobytes())
    print("Recording saved to", FILENAME)
def transcribe_audio():
    """Uses Whisper AI to transcribe recorded audio."""
    result = model.transcribe(FILENAME)
    return result["text"].strip()

def analyze_sentiment(text):
    """Sends transcribed text to Gemini for sentiment analysis."""
    chat_history = [types.Content(role="user", parts=[types.Part.from_text(text=text)])]
    
    ai_response = ""
    for chunk in client.models.generate_content_stream(
        model=model_name, contents=chat_history, config=generate_content_config
    ):
        ai_response += chunk.text
    
    return ai_response

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def process():
    record_audio()
    transcription = transcribe_audio()
    if not transcription:
        return jsonify({"error": "No voice detected, try again."})
    
    analysis = analyze_sentiment(transcription)
    return jsonify({"transcription": transcription, "analysis": analysis})

if __name__ == "__main__":
    app.run(debug=True)
