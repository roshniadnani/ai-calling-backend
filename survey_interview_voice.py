
import requests
import os

# 🔊 Function to speak a line using ElevenLabs
def speak(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/zWRDoH56JB9twPHdkksW"
    headers = {
        "xi-api-key": "sk_edd3176f7b6dd2ec4902a2001883c9bf24d5ff4b8022db1a",
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
        with open("speak_response.mp3", "wb") as f:
            f.write(response.content)
        os.system("start speak_response.mp3")
    else:
        print("❌ Failed to generate voice:", response.text)


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai

openai.api_key = "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"

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("AI_Call_Form").sheet1

questions = [
    "What is your full name?",
    "What is your home address?",
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

answers = []
print("\n🤖 Desiree: Hello! I’m calling to complete your insurance home survey. Let’s get started.\n")
speak("Hello! I’m calling to complete your insurance home survey. Let’s get started.")

def get_polite_reask(question):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are Desiree, an insurance survey caller. If a user skips a question or gives unclear information, gently rephrase and ask again in a polite and friendly tone."},
            {"role": "user", "content": f"The user skipped or didn't answer the question: '{question}'. Please re-ask it politely."}
        ]
    )
    return response.choices[0].message.content.strip()

for q in questions:
    print("🤖 Desiree:", q)
    speak(q)
    user_input = input("👤 You: ").strip()

    while user_input == "" or len(user_input.split()) < 1:
        polite_retry = get_polite_reask(q)
        print("🤖 Desiree (politely re-asking):", polite_retry)
        speak(polite_retry)
        user_input = input("👤 You: ").strip()

    answers.append(user_input)

sheet.append_row(answers)
thank_you = "Thank you! Your answers have been saved to the Google Sheet."
print("\n✅", thank_you)
speak(thank_you)
