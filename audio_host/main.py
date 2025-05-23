from fastapi import FastAPI, Response
import os
from twilio.rest import Client
import openai
from dotenv import load_dotenv

load_dotenv()  # Load .env file

# Twilio credentials
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE")

# OpenAI GPT API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Twilio client
client = Client(account_sid, auth_token)

# GPT conversation state
gpt_conversation = [
    {"role": "system", "content": "You are Desiree, a friendly insurance agent doing a home survey. Ask short and specific questions and do not chit-chat."},
    {"role": "user", "content": "Begin the survey call."}
]

# FastAPI application setup
app = FastAPI()

@app.get("/twiml")
async def twiml():
    # Ask GPT for the next line
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=gpt_conversation
    )
    reply = response['choices'][0]['message']['content']
    gpt_conversation.append({"role": "assistant", "content": reply})

    # Build TwiML with <Say> to speak the reply
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say voice="alice">{reply}</Say>
    </Response>"""
    return Response(content=twiml, media_type="application/xml")

@app.get("/make-call/{to_number}")
def make_call(to_number: str):
    call = client.calls.create(
        to=to_number,
        from_=twilio_number,
        url="https://ai-calling-backend.onrender.com/twiml"  # this hits your /twiml route
    )
    return {"message": "Call initiated", "call_sid": call.sid}
