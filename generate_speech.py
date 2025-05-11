import requests

# Replace with your correct ElevenLabs API key and voice ID
api_key = "sk_eb35891891b639b2337526f9dae63157abdf3257be9118b0"  # Your ElevenLabs API Key
voice_id = "zWRDoH56JB9twPHdkksW"  # Desiree's Voice ID (replace with your actual voice ID)

# Function to generate speech using ElevenLabs API
def generate_speech(text, voice_id=voice_id, api_key=api_key):
    url = "https://api.elevenlabs.io/v1/text-to-speech/generate"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice": voice_id  # Use Desiree's voice ID
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

# Example usage to generate speech (you can replace this text with anything you need for your call)
script = """
Hello, this is Desiree calling from Millennium by Exceedance. We are performing home inspections for your insurance company. I need just a few minutes of your time.

First, can you confirm if the smoke detectors in your home are working? (Yes / No / Unknown)

What year was your home built?

Do you have stairs in your home? (Yes / No)

Is there a pool on your property? (Yes / No)

Can you tell me about the flooring type in your house?

Do you have any pets in your home? (Yes / No)

We also need to know the type of heating system in your home. Is it gas, electric, or something else?

Lastly, could you confirm if your home has a basement? (Yes / No)
"""

# Generate speech using ElevenLabs
audio_path = generate_speech(script)
print(f"Audio generated and saved at: {audio_path}")
