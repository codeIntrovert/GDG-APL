import pyttsx3
import sounddevice as sd
import numpy as np
import whisper
import wave
from google import genai
from google.genai import types
import keys

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
DURATION = 30  # 30 seconds max input
FILENAME = "input.wav"

def record_audio():
    """Records audio for 30 seconds and saves it to a file."""
    print("\n🎤 Recording... Speak now (30 sec max)")
    audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype=np.int16)
    sd.wait()
    print("✅ Recording complete. Processing...")
    
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

def analyze_sentiment(text):
    """Sends transcribed text to Gemini for sentiment analysis."""
    print("Analyzing sentiment...")
    chat_history = [types.Content(role="user", parts=[types.Part.from_text(text=text)])]
    
    ai_response = ""
    for chunk in client.models.generate_content_stream(
        model=model_name, contents=chat_history, config=generate_content_config
    ):
       # print(chunk.text, end="", flush=True)
        ai_response += chunk.text
    
    print("\n")
    return ai_response

def sentiment_analysis():
    """Records, transcribes, and analyzes sentiment."""
    record_audio()
    user_input = transcribe_audio()
    
    if not user_input:
        print("❌ No voice detected, try again.")
        return
    
    analysis = analyze_sentiment(user_input)
    print("Sentiment Analysis:\n", analysis)

if __name__ == "__main__":
    sentiment_analysis()
