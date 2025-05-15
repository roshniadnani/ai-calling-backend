from fastapi import FastAPI, Response, HTTPException
import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# GPT conversation state (initial conversation)
gpt_conversation = [
    {"role": "system", "content": "You are Desiree, a friendly insurance agent doing a home survey. Ask short and specific questions and do not chit-chat."},
    {"role": "user", "content": "Begin the survey call."}
]

# FastAPI application setup
app = FastAPI()

@app.get("/twiml")
async def twiml():
    try:
        # Generate the next line using OpenAI API
        response = openai.chat_completions.create(
            model="gpt-4",  # Use the model you prefer (e.g., "gpt-4")
            messages=gpt_conversation
        )

        # Extract the response text from GPT
        reply = response['choices'][0]['message']['content']
        gpt_conversation.append({"role": "assistant", "content": reply})

        # Build the TwiML response with the generated reply
        speech_url = "https://desiree-voice-files.s3.eu-north-1.amazonaws.com/desiree_intro.mp3"  # Replace with actual Desiree's voice audio URL
        
        # Create the TwiML XML response to be sent back to Twilio
        twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Say>{reply}</Say>  <!-- This will speak the GPT-generated response -->
            <Play>{speech_url}</Play> <!-- Optional, if you want to play Desiree's intro voice -->
        </Response>"""
        
        return Response(content=twiml, media_type="application/xml")
    
    except Exception as e:
        print(f"Error processing TwiML: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing TwiML: {str(e)}")
