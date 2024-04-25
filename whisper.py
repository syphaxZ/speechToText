import whisper
model = whisper.load_model("medium")
result = model.transcribe("audio2.mp3")
print(result["text"])