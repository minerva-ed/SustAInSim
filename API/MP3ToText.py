from deepgram import Deepgram
import asyncio, json
import sys

# Your Deepgram API Key
DEEPGRAM_API_KEY = '81b04dbabf586e94fe17c59debfb7d743467e1ae'

# Location of the file you want to transcribe. Should include filename and extension.
# Example of a local file: ../../Audio/life-moves-pretty-fast.wav
# Example of a remote file: https://static.deepgram.com/examples/interview_speech-analytics.wav
FILE = 'output.wav'

# Mimetype for the file you want to transcribe
# Include this line only if transcribing a local file
# Example: audio/wav
MIMETYPE = 'wav'

async def main(DEEPGRAM_API_KEY,FILE,MIMETYPE):

  # Initialize the Deepgram SDK
  deepgram = Deepgram(DEEPGRAM_API_KEY)

  # Check whether requested file is local or remote, and prepare source
  if FILE.startswith('http'):
    # file is remote
    # Set the source
    source = {
      'url': FILE
    }
  else:
    # file is local
    # Open the audio file
    audio = open(FILE, 'rb')

    # Set the source
    source = {
      'buffer': audio,
      'mimetype': MIMETYPE
    }

  # Send the audio to Deepgram and get the response
  response = await asyncio.create_task(
    deepgram.transcription.prerecorded(
      source,
      {
        'smart_format': True,
        'model': 'nova-2',
      }
    )
  )

  # Write the response to the console
  print(json.dumps(response, indent=4))

  # Write only the transcript to the console
  # Extract the transcript
  transcript = response['results']['channels'][0]['alternatives'][0]['transcript']

    # Write the transcript to a text file
  with open('transcript.txt', 'w') as file:
    file.write(transcript)

try:
  print()
except Exception as e:
  exception_type, exception_object, exception_traceback = sys.exc_info()
  line_number = exception_traceback.tb_lineno
  print(f'line {line_number}: {exception_type} - {e}')