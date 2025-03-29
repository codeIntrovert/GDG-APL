import whisper

model = whisper.load_model("tiny.en")
result = model.transcribe("test.mp3")
print("\n\n"+result["text"])