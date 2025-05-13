import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ✅ Optional: Setup for GPT use if needed in future
import openai
openai.api_key = "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"

# STEP 1: SETUP GOOGLE SHEET ACCESS
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("AI_Call_Form").sheet1

# STEP 2: DESIREE'S CALL SCRIPT QUESTIONS (from your PDF scripts)
questions = [
    "What is your full name?",
    "What is your home address?",
    "What is your current insurance provider?",
    "Are all your smoke detectors working?",
    "Do you know the name of the nearest fire station?",
    "When was your roof last replaced?",
    "How many kitchens do you have? What size?",
    "What is your kitchen countertop made of?",
    "How many bathrooms do you have? What size?",
    "What type of heating system does your home use?",
    "Do you have any pets? If yes, what kind?",
    "Is your home air conditioned? (Yes/No)",
    "Do you have a basement? Is it finished?",
    "Do you have a monitored fire/security alarm system? Which company monitors it?"
]

# STEP 3: ASK QUESTIONS AND STORE ANSWERS
answers = []
print("\n🤖 Desiree: Hello! I’m calling to complete your insurance home survey. Let’s get started.\n")

for q in questions:
    print("🤖 Desiree:", q)
    user_response = input("👤 You: ")
    answers.append(user_response)

# STEP 4: SAVE TO GOOGLE SHEET
sheet.append_row(answers)
print("\n✅ Thank you! Your answers have been saved to the Google Sheet.")
