import requests
import io
import pygame

#text="Due to the range of API calls and background computations occurring, as well as interactions between the different agents, our program runtime is over a minute. We are looking to optimize it, but were unable to achieve significant improvements with either multithreading or asynchronous calls. We hope to increase the efficiency of this program to make it more efficient and scalable in the future."

def textToSpeech(TEXT,voice):
    # Initialize pygame mixer
    pygame.mixer.init()

    text=str(TEXT)

    # API request
    response = requests.post(
        'https://api.v6.unrealspeech.com/stream',
        headers={
            'Authorization': 'Bearer 3a050GSmB7NN9BmKVmWyuoE3h2sRALnChaScRnIOqQQTF3twJ6L9Wz'
        },
        json={
            'Text': TEXT,
            'VoiceId': voice,
            'Bitrate': '192k',
            'Speed': '0',
            'Pitch': '1',
            'Codec': 'libmp3lame',
        }
    )
    print(response.status_code)
    # Check if the response is valid
    if response.status_code == 200:
        # Load the audio data into a BytesIO buffer
        audio_data = io.BytesIO(response.content)

        # Load this buffer using pygame
        pygame.mixer.music.load(audio_data)
        pygame.mixer.music.play()

        # Keep the script running until the audio is played
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    else:
        print("Failed to retrieve audio data")

#textToSpeech(text)
