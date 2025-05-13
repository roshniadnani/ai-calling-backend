import openai
import requests
import os
import time

# ✅ Keys & IDs
openai.api_key = "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"
eleven_api_key = "sk_edd3176f7b6dd2ec4902a2001883c9bf24d5ff4b8022db1a"
voice_id = "zWRDoH56JB9twPHdkksW"  # Desiree

# 📢 Function to speak via ElevenLabs
def speak(text):
    print(f"🤖 Desiree: {text}")
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
        with open("ai_question.mp3", "wb") as f:
            f.write(response.content)
        os.system("start ai_question.mp3")  # For Windows
    else:
        print("❌ Voice generation failed:", response.text)

# 🤖 Function to ask GPT next question
def get_next_question(history):
    messages = [{"role": "system", "content": "You are Desiree, a friendly insurance surveyor. Follow the home inspection script strictly. Don’t make chit-chat. Keep questions short, professional, and specific to home inspection. If survey is done, say so."}]
    for q, a in history:
        messages.append({"role": "user", "content": f"Q: {q}\nA: {a}"})
    messages.append({"role": "user", "content": "Ask next question."})

    reply = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    return reply.choices[0].message.content.strip()

# 🔁 MAIN LOOP
conversation = []
current_q = "Hi! I'm Desiree from Millennium by Exceedance. May I confirm your full name and address?"

while True:
    speak(current_q)
    time.sleep(1)
    user_input = input("👤 You: ")
    conversation.append((current_q, user_input))

    if "done" in user_input.lower() or "that's all" in user_input.lower():
        speak("Thank you! That concludes our home insurance survey.")
        break

    current_q = get_next_question(conversation)
