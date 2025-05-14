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
