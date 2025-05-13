import openai
import requests
import os
import time
import uuid

# ✅ Set your API keys
openai.api_key = "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"
eleven_api_key = "sk_edd3176f7b6dd2ec4902a2001883c9bf24d5ff4b8022db1a"
voice_id = "zWRDoH56JB9twPHdkksW"  # Desiree's voice

# ✅ Pre-written American demo responses
auto_answers = [
    "My name is Jessica Morgan and I live at 3425 Maplewood Drive, Springfield, Illinois 62704.",
    "It's State Farm.",
    "Yes, all of them are working perfectly.",
    "Yes, Station 12 – about 2.5 miles away.",
    "The roof was replaced in 2017 after a hailstorm.",
    "One kitchen, around 150 square feet.",
    "Granite countertops.",
    "Two bathrooms – one full and one half bath.",
    "Gas furnace with forced air.",
    "Yes, I have a golden retriever named Max.",
    "Yes, central air throughout the home.",
    "Yes, a finished basement with a bar and lounge area.",
    "Yes, it’s monitored by ADT security."
]

# ✅ First question
questions = [
    "Hi! I'm Desiree from Millennium by Exceedance. May I confirm your full name and address?",
    "What is your current insurance provider?",
    "Are all your smoke detectors working?",
    "Do you know the name of the nearest fire station?",
    "When was your roof last replaced?",
    "How many kitchens do you have? What size?",
    "What is your kitchen countertop made of?",
    "How many bathrooms do you have? What size?",
    "What type of heating system does your home use?",
    "Do you have any pets? If yes, what kind?",
    "Is your home air conditioned? (Yes/No)",
    "Do you have a basement? Is it finished?",
    "Do you have a monitored fire/security alarm system? Which company monitors it?"
]

# ✅ ElevenLabs Text-to-Speech
def speak(text):
    print(f"\n🤖 Desiree: {text}")
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
        filename = f"question_{uuid.uuid4().hex[:6]}.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)
        os.system(f"start {filename}")
    else:
        print("❌ Voice generation failed:", response.text)

# ✅ Begin demo loop
for i in range(len(questions)):
    speak(questions[i])
    print(f"👤 You: {auto_answers[i]}")
    time.sleep(1)

# ✅ End message
speak("Thank you. That concludes our home insurance survey. Have a great day!")
