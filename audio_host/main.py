from fastapi import FastAPI, Request
from fastapi.responses import Response
from twilio.rest import Client
import openai

app = FastAPI()

# ✅ Twilio Credentials (Final, no edits)
account_sid = "ACfe9f45e6152aa5a6e6325613a2f6ae66"
auth_token = "eafc38a7a29748c8ea61f34246c6a866"
twilio_number = "+16813346078"
client = Client(account_sid, auth_token)

# ✅ OpenAI API Key (Final, no edits)
openai.api_key = "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"

# ✅ 1st question for the call
gpt_conversation = [
    {"role": "system", "content": "You are Desiree, a friendly insurance agent doing a home survey. Ask short and specific questions and do not chit-chat."},
    {"role": "user", "content": "Begin the survey call."}
]

@app.get("/twiml")
async def twiml():
    # Ask GPT for the next line
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=gpt_conversation
    )
    reply = response['choices'][0]['message']['content']
    gpt_conversation.append({"role": "assistant", "content": reply})

    # Build TwiML with <Say>
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
