import requests

# New ElevenLabs API key and voice ID
api_key = "sk_edd3176f7b6dd2ec4902a2001883c9bf24d5ff4b8022db1a"  # Your new API Key
voice_id = "zWRDoH56JB9twPHdkksW"  # Desiree's Voice ID (replace with your actual voice ID)

# Function to generate speech using ElevenLabs API
def generate_speech(text, voice_id=voice_id, api_key=api_key):
    url = "https://api.elevenlabs.io/v1/text-to-speech/generate"
    headers = {
        "Authorization": f"Bearer {api_key}",  # Make sure this API key is correct
        "Content-Type": "application/json"
    }
    data = {
        "text": text,       # The text to be converted to speech
        "voice": voice_id   # Desiree's voice ID
    }

    # Make the API request to generate speech
    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        # Save the response content (audio) to a file
        audio_file_path = "output_audio.wav"
        with open(audio_file_path, "wb") as f:
            f.write(response.content)
        print(f"Audio generated and saved at: {audio_file_path}")
        return audio_file_path
    else:
        print("Error generating speech:", response.json())
        return None
