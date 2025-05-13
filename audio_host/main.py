from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from twilio.rest import Client

app = FastAPI()

# Optional CORS (can leave it if not using frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

# ✅ Twilio Credentials (secure via env in production)
account_sid = "ACfe9f45e6152aa5a6e6325613a2f6ae66"
auth_token = "eafc38a7a29748c8ea61f34246c6a866"
twilio_number = "+16813346078"
client = Client(account_sid, auth_token)

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit-survey/", response_class=HTMLResponse)
async def submit_survey(request: Request, name: str = Form(...), email: str = Form(...)):
    return templates.TemplateResponse("result.html", {"request": request, "name": name, "email": email})

@app.get("/twiml")
def twiml_response():
    twiml = """
    <Response>
        <Play>https://cdn.jsdelivr.net/gh/roshniadnani/ai-calling-audio/output_audio.wav.mp3</Play>
    </Response>
    """
    return Response(content=twiml.strip(), media_type="application/xml")

@app.get("/make-call/{to_number}")
def make_call(to_number: str):
    twiml_url = "https://ai-calling-backend.onrender.com/twiml"
    call = client.calls.create(
        to=to_number,
        from_=twilio_number,
        url=twiml_url
    )
    return {"message": "Call initiated", "call_sid": call.sid}
