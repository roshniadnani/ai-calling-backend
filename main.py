from fastapi import FastAPI, Response
import os
from twilio.rest import Client
import openai
import boto3
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio credentials
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE")

# OpenAI GPT API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# AWS S3 setup
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

# Initialize Twilio client
client = Client(account_sid, auth_token)

# GPT conversation state
gpt_conversation = [
    {"role": "system", "content": "You are Desiree, a friendly insurance agent doing a home survey. Ask short and specific questions and do not chit-chat."},
    {"role": "user", "content": "Begin the survey call."}
]

# FastAPI application setup
app = FastAPI()

# Root route to confirm the server is up
@app.get("/")
async def root():
    return {"message": "FastAPI is running!"}

# TwiML route for generating audio response (from S3)
@app.get("/twiml")
async def twiml():
    # Ask GPT for the next line of the conversation
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=gpt_conversation
    )
    reply = response['choices'][0]['message']['content']
    gpt_conversation.append({"role": "assistant", "content": reply})

    # Use the S3 URL of Desiree's intro audio
    speech_url = "https://desiree-voice-files.s3.eu-north-1.amazonaws.com/desiree_intro.mp3"
    
    # Build TwiML with <Play> to play the audio from S3
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Play>{speech_url}</Play>
    </Response>"""
    
    return Response(content=twiml, media_type="application/xml")

# Make call route to initiate a call
@app.get("/make-call/{to_number}")
def make_call(to_number: str):
    call = client.calls.create(
        to=to_number,
        from_=twilio_number,
        url="https://your-app-url/twiml"  # Replace with your actual deployed URL
    )
    return {"message": "Call initiated", "call_sid": call.sid}
