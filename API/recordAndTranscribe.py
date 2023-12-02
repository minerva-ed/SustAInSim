from audioToMP3 import record_audio
from MP3ToText import main as transcribe_audio
import asyncio


def record_and_transcribe():
    # Record audio and save as MP3
    wav_file_name=record_audio()

    #print("step 1 done")

    # Transcribe the recorded audio
    asyncio.run(transcribe_audio('81b04dbabf586e94fe17c59debfb7d743467e1ae',
                                 wav_file_name,
                                 'wav'))

#record_and_transcribe()
