import os
import whisper

print("✅ Starting Conversation Agent")

# Show directory & files
cwd = os.getcwd()
print(f"📁 Working Directory: {cwd}")
print(f"📄 Files: {os.listdir(cwd)}")

# Transcribe intro audio
print("🎙 Transcribing desiree_intro.mp3...")
try:
    model = whisper.load_model("base")
    result = model.transcribe("desiree_intro.mp3")
    print("📜 Transcript:", result["text"])
except Exception as e:
    print("❌ Error during transcription:", e)
