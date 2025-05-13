from fastapi import FastAPI, Response
import os
from twilio.rest import Client
import openai
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio credentials from environment variables
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE")

# OpenAI GPT API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

# ElevenLabs credentials from environment variables
eleven_api_key = os.getenv("ELEVENLABS_API_KEY")
voice_id = os.getenv("ELEVENLABS_VOICE_ID")

# Initialize Twilio client
client = Client(account_sid, auth_token)

# GPT conversation state - initiate conversation
gpt_conversation = [
    {"role": "system", "content": "You are Desiree, a friendly insurance agent doing a home survey. Ask short and specific questions and do not chit-chat."},
    {"role": "user", "content": "Begin the survey call."}
]

# Initialize FastAPI app
app = FastAPI()

# Root route to handle "/"
@app.get("/")
async def root():
    return {"message": "FastAPI is running!"}

# Function to generate Desiree's voice using ElevenLabs API
def generate_speech(text):
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
        # Save the speech as an MP3 file
        filename = "desiree_speech.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename
    else:
        print(f"❌ Error generating speech: {response.text}")
        return None

@app.get("/twiml")
async def twiml():
    # Ask GPT for the next line of the conversation
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=gpt_conversation
    )
    reply = response['choices'][0]['message']['content']
    gpt_conversation.append({"role": "assistant", "content": reply})

    # Generate Desiree's speech using ElevenLabs
    speech_file = generate_speech(reply)
    if speech_file:
        # Use Twilio's <Play> verb to play the generated speech file
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Play>{speech_file}</Play>  <!-- Play the generated audio file -->
        </Response>"""
    else:
        # In case speech generation fails, fall back to default Twilio voice
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Say voice="alice">{reply}</Say>
        </Response>"""
    
    return Response(content=twiml, media_type="application/xml")

@app.get("/make-call/{to_number}")
def make_call(to_number: str):
    # Initiate the call via Twilio
    call = client.calls.create(
        to=to_number,
        from_=twilio_number,
        url="http://127.0.0.1:8000/twiml"  # This triggers the /twiml route
    )
    return {"message": "Call initiated", "call_sid": call.sid}
