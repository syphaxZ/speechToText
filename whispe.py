import whisper

def transcribe_audio(audio_path):
    # Load the Whisper medium model
    model = whisper.load_model("medium")
    
    # Transcribe the audio from the provided path
    result = model.transcribe(audio_path)
    
    # Return the transcribed text
    return result["text"]

# Example usage:
transcript = transcribe_audio()
print(transcript)
