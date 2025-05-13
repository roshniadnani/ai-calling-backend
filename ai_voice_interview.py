import whisper
import openai
import requests
import sounddevice as sd
import scipy.io.wavfile as wav
import os
import tempfile

# SETUP 🔐
openai.api_key = "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"
eleven_api_key = "sk_edd3176f7b6dd2ec4902a2001883c9bf24d5ff4b8022db1a"
voice_id = "zWRDoH56JB9twPHdkksW"

# ElevenLabs generation
def speak(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": eleven_api_key,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open("ai_reply.mp3", "wb") as f:
            f.write(response.content)
        os.system("start ai_reply.mp3")  # plays on Windows
    else:
        print("❌ Error from ElevenLabs:", response.text)

# Record voice using mic
def record_voice():
    fs = 44100  # Sample rate
    duration = 7  # seconds
    print("🎤 Speak now...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        wav.write(tmpfile.name, fs, recording)
        return tmpfile.name

# Transcribe audio using Whisper
def transcribe_audio(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    return result["text"]

# GPT conversation logic
def ask_gpt(prev_q, answer):
    prompt = f"""You are Desiree, a friendly insurance agent doing a home survey. 
You just asked: "{prev_q}" 
User replied: "{answer}" 
Give the next appropriate survey question only."""
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're conducting a home insurance survey in a friendly tone. Keep each question short and direct."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# MAIN LOOP 🔁
questions_asked = []
current_q = "Hello! I'm Desiree from Millennium Insurance. May I begin your home survey by confirming your full name and home address?"

while True:
    speak(current_q)
    audio_file = record_voice()
    user_answer = transcribe_audio(audio_file)
    print(f"📝 You said: {user_answer}")
    
    questions_asked.append((current_q, user_answer))
    
    # STOP condition
    if "stop" in user_answer.lower() or "that's all" in user_answer.lower():
        speak("Thank you! That completes our survey.")
        break

    # Get next question
    current_q = ask_gpt(current_q, user_answer)
