import requests

api_key = "sk_edd3176f7b6dd2ec4902a2001883c9bf24d5ff4b8022db1a"
voice_id = "zWRDoH56JB9twPHdkksW"
text = "Hi, this is Desiree from Millennium Insurance. Just testing my voice!"

url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
headers = {
    "xi-api-key": api_key,
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
    with open("test_reply.mp3", "wb") as f:
        f.write(response.content)
    print("✅ Test voice saved as test_reply.mp3")
else:
    print("❌ Error:", response.text)
