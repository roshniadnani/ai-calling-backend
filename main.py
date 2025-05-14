from fastapi import FastAPI, HTTPException, Response
import os
from twilio.rest import Client
import openai
from dotenv import load_dotenv
import boto3

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

# Debugging: Print the Twilio credentials to check if they are loaded correctly
print(f"Twilio Account SID: {account_sid}")
print(f"Twilio Auth Token: {auth_token}")
print(f"Twilio Phone: {twilio_number}")

@app.get("/")
async def root():
    return {"message": "FastAPI is running!"}

@app.get("/twiml")
async def twiml():
    try:
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
            <Play>{https://desiree-voice-files.s3.eu-north-1.amazonaws.com/desiree_intro.mp3}</Play>
        </Response>"""
        
        return Response(content=twiml, media_type="application/xml")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing TwiML: {str(e)}")

@app.get("/make-call/{to_number}")
def make_call(to_number: str):
    try:
        # Log the received phone number
        print(f"Making call to: {to_number}")
        
        # Attempt to initiate the call
        call = client.calls.create(
            to=to_number,
            from_=twilio_number,
            url="https://ai-calling-backend.onrender.com/twiml"  # Updated Render URL for production
        )
        
        print(f"Call SID: {call.sid}")  # Log the Call SID for confirmation
        
        return {"message": "Call initiated", "call_sid": call.sid}
    
    except Exception as e:
        print(f"Error initiating call: {str(e)}")  # Log the error details
        raise HTTPException(status_code=500, detail=f"Error initiating call: {str(e)}")
