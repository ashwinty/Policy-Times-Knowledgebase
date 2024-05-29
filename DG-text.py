# import os
# import logging
# import time
# import traceback
# from deepgram import DeepgramClient, PrerecordedOptions, FileSource
# from dotenv import load_dotenv
# from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
# import httpx
# from pydub import AudioSegment
# import json

# # Load environment variables
# load_dotenv()

# # Set up logging
# logging.basicConfig(level=logging.INFO)

# # Deepgram API key
# DG_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# # Retry decorator with tenacity
# @retry(
#     stop=stop_after_attempt(3),  # Retry up to 3 times
#     wait=wait_fixed(5),  # Wait 5 seconds between retries
#     retry=retry_if_exception_type(httpx.RequestError)  # Only retry on request errors
# )
# def transcribe_audio_file(buffer_data, model="nova-2"):
#     try:
#         if not DG_API_KEY:
#             raise ValueError("Deepgram API key not found in environment variables.")

#         # Create a Deepgram client using the API key
#         deepgram = DeepgramClient(DG_API_KEY)

#         payload: FileSource = {
#             "buffer": buffer_data,
#         }

#         # Configure Deepgram options for audio analysis
#         options = PrerecordedOptions(
#             model=model,
#             smart_format=True,
#         )

#         # Call the transcribe_file method with the text payload and options
#         response = deepgram.listen.prerecorded.v("1").transcribe_file(
#             payload, options, timeout=httpx.Timeout(60.0)
#         )

#         # Return the transcript
#         return response.to_json()

#     except Exception as e:
#         logging.error(f"Error transcribing audio file: {e}")
#         traceback.print_exc()  # Print the full error traceback
#         return None

# def split_audio(file_path, chunk_length_ms=60000):
#     audio = AudioSegment.from_file(file_path)
#     chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
#     return chunks

# # Paths for audio and text directories
# audio_directory = "Audio"
# text_directory = "Text2"

# # Ensure the text directory exists
# os.makedirs(text_directory, exist_ok=True)

# # Process each audio file in the audio directory
# for audio_filename in os.listdir(audio_directory):
#     if audio_filename.endswith(".mp3"):
#         audio_path = os.path.join(audio_directory, audio_filename)
#         logging.info(f"Transcribing file: {audio_path}")
        
#         chunks = split_audio(audio_path)

#         full_transcript = ""
#         for i, chunk in enumerate(chunks):
#             logging.info(f"Transcribing chunk {i+1}/{len(chunks)} of {audio_filename}")
            
#             chunk_buffer = chunk.export(format="mp3").read()
#             transcript = transcribe_audio_file(chunk_buffer)
            
#             if transcript:
#                 # Log the response before attempting JSON parsing
#                 logging.info(f"Transcript response: {transcript}")

#                 # Split concatenated JSON objects and parse them individually
#                 for json_obj in transcript.split('}'):
#                     if json_obj.strip():
#                         json_data = json_obj + '}'
#                         try:
#                             data = json.loads(json_data)
#                             if 'results' in data:
#                                 for result in data['results']['channels']:
#                                     for alt in result['alternatives']:
#                                         full_transcript += alt['transcript'] + '\n'
#                         except json.JSONDecodeError as e:
#                             logging.error(f"JSON decoding error: {e}")

#         # Save the transcript to the text directory with the same base name as the audio file
#         text_filename = os.path.splitext(audio_filename)[0] + ".txt"
#         text_path = os.path.join(text_directory, text_filename)
        
#         with open(text_path, "w") as text_file:
#             text_file.write(full_transcript)
        
#         logging.info(f"Transcript saved to: {text_path}")




















import os
import logging
import time
import traceback
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import httpx
from pydub import AudioSegment

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Deepgram API key
DG_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# Retry decorator with tenacity
@retry(
    stop=stop_after_attempt(3),  # Retry up to 3 times
    wait=wait_fixed(5),  # Wait 5 seconds between retries
    retry=retry_if_exception_type(httpx.RequestError)  # Only retry on request errors
)
def transcribe_audio_file(buffer_data, model="nova-2"):
    try:
        if not DG_API_KEY:
            raise ValueError("Deepgram API key not found in environment variables.")

        # Create a Deepgram client using the API key
        deepgram = DeepgramClient(DG_API_KEY)

        payload: FileSource = {
            "buffer": buffer_data,
        }

        # Configure Deepgram options for audio analysis
        options = PrerecordedOptions(
            model=model,
            smart_format=True,
        )

        # Call the transcribe_file method with the text payload and options
        response = deepgram.listen.prerecorded.v("1").transcribe_file(
            payload, options, timeout=httpx.Timeout(60.0)
        )

        # Return the transcript
        return response.to_json()

    except Exception as e:
        logging.error(f"Error transcribing audio file: {e}")
        traceback.print_exc()  # Print the full error traceback
        return None

def split_audio(file_path, chunk_length_ms=60000):
    audio = AudioSegment.from_file(file_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]
    return chunks

# Paths for audio and text directories
audio_directory = "Audio"
text_directory = "Text2"

# Ensure the text directory exists
os.makedirs(text_directory, exist_ok=True)

# Process each audio file in the audio directory
for audio_filename in os.listdir(audio_directory):
    if audio_filename.endswith(".mp3"):
        audio_path = os.path.join(audio_directory, audio_filename)
        logging.info(f"Transcribing file: {audio_path}")
        
        chunks = split_audio(audio_path)

        full_transcript = ""
        for i, chunk in enumerate(chunks):
            logging.info(f"Transcribing chunk {i+1}/{len(chunks)} of {audio_filename}")
            
            chunk_buffer = chunk.export(format="mp3").read()
            transcript = transcribe_audio_file(chunk_buffer)
            
            if transcript:
                full_transcript += transcript

        # Save the transcript to the text directory with the same base name as the audio file
        text_filename = os.path.splitext(audio_filename)[0] + ".txt"
        text_path = os.path.join(text_directory, text_filename)
        
        with open(text_path, "w") as text_file:
            text_file.write(full_transcript)
        
        logging.info(f"Transcript saved to: {text_path}")
