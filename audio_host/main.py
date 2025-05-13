from fastapi import FastAPI
from fastapi.responses import Response
from twilio.rest import Client

app = FastAPI()

@app.get("/twiml")
def twiml_response():
    twiml = """
    <Response>
        <Say voice="Polly.Joanna">
            Hello, this is Desiree calling from Millennium Information Services on behalf of your insurance provider.
            This is a test call from our AI-powered voice agent. If you're hearing this, the system is working.
            Thank you and have a great day!
        </Say>
    </Response>
    """
    return Response(content=twiml.strip(), media_type="application/xml")

@app.get("/make-call/{to_number}")
def make_call(to_number: str):
    account_sid = "ACfe9f45e6152aa5a6e6325613a2f6ae66"
    auth_token = "eafc38a7a29748c8ea61f34246c6a866"
    twilio_number = "+16813346078"
    twiml_url = "https://ai-calling-backend.onrender.com/twiml"

    client = Client(account_sid, auth_token)

    call = client.calls.create(
        to=to_number,
        from_=twilio_number,
        url=twiml_url
    )

    return {"message": "Call initiated", "sid": call.sid}
