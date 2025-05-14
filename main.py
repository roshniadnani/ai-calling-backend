from fastapi import FastAPI, Response
import os
import openai
import requests
from twilio.rest import Client
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load environment variables from .env file
load_dotenv()

# Twilio credentials (already provided in your .env file)
account_sid = "ACfe9f45e6152aa5a6e6325613a2f6ae66"  # Your TWILIO_ACCOUNT_SID
auth_token = "eafc38a7a29748c8ea61f34246c6a866"  # Your TWILIO_AUTH_TOKEN
twilio_number = "+16813346078"  # Your Twilio phone number

# OpenAI GPT API key
openai.api_key = "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"  # Your OPENAI_API_KEY

# ElevenLabs credentials
eleven_api_key = "sk_edd3176f7b6dd2ec4902a2001883c9bf24d5ff4b8022db1a"  # Your ELEVENLABS_API_KEY
voice_id = "zWRDoH56JB9twPHdkksW"  # Your ELEVENLABS_VOICE_ID

# Initialize Twilio client
client = Client(account_sid, auth_token)

# GPT conversation state - initiate conversation
gpt_conversation = [
    {"role": "system", "content": "You are Desiree, a friendly insurance agent doing a home survey. Ask short and specific questions and do not chit-chat."},
    {"role": "user", "content": "Begin the survey call."}
]

# Initialize FastAPI app
app = FastAPI()

# Function to authenticate and get Google Sheets client
def get_google_sheets_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client

# Function to save response to Google Sheets
def save_to_google_sheets(question, answer):
    client = get_google_sheets_client()
    sheet = client.open("Home Insurance Survey").sheet1  # Your Google Sheet name
    sheet.append_row([question, answer])

# Function to generate speech using ElevenLabs API
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
        filename = "desiree_speech.mp3"
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename
    else:
        print(f"❌ Error generating speech: {response.text}")
        return None

# Root route for testing
@app.get("/")
async def root():
    return {"message": "FastAPI is running!"}

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
    
    # Save question and answer to Google Sheets
    save_to_google_sheets(gpt_conversation[-2]['content'], reply)

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
