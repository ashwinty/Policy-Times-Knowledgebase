# from pydub import AudioSegment
# import os
# import math
# from google.cloud import speech_v2 as speech
# from google.cloud.speech_v2 import SpeechClient
# from google.cloud.speech_v2.types import cloud_speech
# import io
# import tempfile
# from google.api_core.exceptions import AlreadyExists
# import time
# import logging
# import traceback

# # Set up logging
# logging.basicConfig(level=logging.INFO)

# # Set up your Google Cloud credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "GOOGLE_APPLICATION_CREDENTIALS_JSON.json"

# def split_audio(audio_path, chunk_length_ms):
#     audio = AudioSegment.from_file(audio_path, format="mp3")
#     audio = audio.set_channels(1)  # Convert to mono
#     audio_chunks = []
#     total_length = len(audio)
#     num_chunks = math.ceil(total_length / chunk_length_ms)

#     for i in range(num_chunks):
#         start = i * chunk_length_ms
#         end = min(start + chunk_length_ms, total_length)
#         chunk = audio[start:end]
#         audio_chunks.append(chunk)

#     return audio_chunks

# def transcribe_chunk_v2(chunk, recognizer_name, language_code="en-US"):
#     client = SpeechClient()
#     # Export the chunk to a temporary file
#     with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio_file:
#         chunk.export(temp_audio_file.name, format="wav")
#         temp_audio_file.seek(0)
        
#         config = cloud_speech.RecognitionConfig(
#             auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
#             language_codes=[language_code],
#             model="long",
#         )

#         with io.open(temp_audio_file.name, "rb") as audio_file:
#             content = audio_file.read()
#             if len(content) > 10 * 1024 * 1024:  # Check if the chunk size exceeds 10 MB
#                 raise ValueError("Chunk size exceeds 10 MB limit")

#         request = cloud_speech.RecognizeRequest(
#             recognizer=recognizer_name,
#             config=config,
#             content=content
#         )

#         response = client.recognize(request=request)

#         transcripts = [result.alternatives[0].transcript for result in response.results]
#         return " ".join(transcripts)

# def transcribe_audio_file(audio_path, recognizer_name, chunk_length_ms=15 * 1000):  # Reduced chunk size to 15 seconds
#     chunks = split_audio(audio_path, chunk_length_ms)
#     full_transcript = ""
    
#     for i, chunk in enumerate(chunks):
#         logging.info(f"Processing chunk {i + 1}/{len(chunks)}...")
#         start_time = time.time()
#         try:
#             transcript = transcribe_chunk_with_retry(chunk, recognizer_name)
#             full_transcript += transcript + " "
#         except ValueError as e:
#             logging.error(f"Chunk {i + 1} skipped due to size limit: {e}")
#         except Exception as e:
#             logging.error(f"Error processing chunk {i + 1}: {e}")
#             traceback.print_exc()  # Print the full error traceback
#         end_time = time.time()
#         logging.info(f"Chunk {i + 1} processed in {end_time - start_time:.2f} seconds")
    
#     return full_transcript

# def transcribe_chunk_with_retry(chunk, recognizer_name, retries=3, delay=5):
#     for attempt in range(retries):
#         try:
#             return transcribe_chunk_v2(chunk, recognizer_name)
#         except Exception as e:
#             logging.error(f"Error transcribing chunk: {e}")
#             if attempt < retries - 1:
#                 logging.info(f"Retrying in {delay} seconds...")
#                 time.sleep(delay)
#             else:
#                 raise

# def create_recognizer_if_not_exists(project_id: str, recognizer_id: str) -> cloud_speech.Recognizer:
#     client = SpeechClient()
#     recognizer_name = f"projects/{project_id}/locations/global/recognizers/{recognizer_id}"

#     try:
#         request = cloud_speech.CreateRecognizerRequest(
#             parent=f"projects/{project_id}/locations/global",
#             recognizer_id=recognizer_id,
#             recognizer=cloud_speech.Recognizer(
#                 default_recognition_config=cloud_speech.RecognitionConfig(
#                     language_codes=["en-US"], model="long"
#                 ),
#             ),
#         )

#         operation = client.create_recognizer(request=request)
#         recognizer = operation.result()

#         logging.info(f"Created Recognizer: {recognizer.name}")
#     except AlreadyExists:
#         logging.info(f"Recognizer already exists: {recognizer_name}")
#         recognizer = client.get_recognizer(name=recognizer_name)

#     return recognizer

# # Replace with your project-specific project ID
# project_id = "groovy-age-420314"
# recognizer_id = "thothica-test123"  # You can define a recognizer ID here
# recognizer_name = f"projects/{project_id}/locations/global/recognizers/{recognizer_id}"

# # Create the recognizer if it doesn't exist
# create_recognizer_if_not_exists(project_id, recognizer_id)

# # Paths for audio and text directories
# audio_directory = "Audio"
# text_directory = "Text"

# # Ensure the text directory exists
# os.makedirs(text_directory, exist_ok=True)

# # Process each audio file in the audio directory
# for audio_filename in os.listdir(audio_directory):
#     if audio_filename.endswith(".mp3"):
#         audio_path = os.path.join(audio_directory, audio_filename)
#         logging.info(f"Transcribing file: {audio_path}")
        
#         transcript = transcribe_audio_file(audio_path, recognizer_name)
        
#         # Save the transcript to the text directory with the same base name as the audio file
#         text_filename = os.path.splitext(audio_filename)[0] + ".txt"
#         text_path = os.path.join(text_directory, text_filename)
        
#         with open(text_path, "w") as text_file:
#             text_file.write(transcript)
        
#         logging.info(f"Transcript saved to: {text_path}")
























from pydub import AudioSegment
import os
import math
from google.cloud import speech_v2 as speech
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech
import io
import tempfile
from google.api_core.exceptions import AlreadyExists

# Set up your Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "GOOGLE_APPLICATION_CREDENTIALS_JSON.json"

def split_audio(audio_path, chunk_length_ms):
    audio = AudioSegment.from_file(audio_path, format="mp3")
    audio = audio.set_channels(1)  # Convert to mono
    audio_chunks = []
    total_length = len(audio)
    num_chunks = math.ceil(total_length / chunk_length_ms)

    for i in range(num_chunks):
        start = i * chunk_length_ms
        end = min(start + chunk_length_ms, total_length)
        chunk = audio[start:end]
        audio_chunks.append(chunk)

    return audio_chunks

def transcribe_chunk_v2(chunk, recognizer_name, language_code="en-US"):
    client = SpeechClient()
    # Export the chunk to a temporary file
    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio_file:
        chunk.export(temp_audio_file.name, format="wav")
        temp_audio_file.seek(0)
        
        config = cloud_speech.RecognitionConfig(
            auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
            language_codes=[language_code],
            model="long",
        )

        with io.open(temp_audio_file.name, "rb") as audio_file:
            content = audio_file.read()
            if len(content) > 10 * 1024 * 1024:  # Check if the chunk size exceeds 10 MB
                raise ValueError("Chunk size exceeds 10 MB limit")

        request = cloud_speech.RecognizeRequest(
            recognizer=recognizer_name,
            config=config,
            content=content
        )

        response = client.recognize(request=request)

        transcripts = [result.alternatives[0].transcript for result in response.results]
        return " ".join(transcripts)

def transcribe_audio_file(audio_path, recognizer_name, chunk_length_ms=60 * 1000):
    chunks = split_audio(audio_path, chunk_length_ms)
    full_transcript = ""
    
    for i, chunk in enumerate(chunks):
        print(f"Processing chunk {i + 1}/{len(chunks)}...")
        try:
            transcript = transcribe_chunk_v2(chunk, recognizer_name)
            full_transcript += transcript + " "
        except ValueError as e:
            print(e)
            print(f"Skipping chunk {i + 1} due to size limit.")

    return full_transcript

def create_recognizer_if_not_exists(project_id: str, recognizer_id: str) -> cloud_speech.Recognizer:
    client = SpeechClient()
    recognizer_name = f"projects/{project_id}/locations/global/recognizers/{recognizer_id}"

    try:
        request = cloud_speech.CreateRecognizerRequest(
            parent=f"projects/{project_id}/locations/global",
            recognizer_id=recognizer_id,
            recognizer=cloud_speech.Recognizer(
                default_recognition_config=cloud_speech.RecognitionConfig(
                    language_codes=["en-US"], model="long"
                ),
            ),
        )

        operation = client.create_recognizer(request=request)
        recognizer = operation.result()

        print("Created Recognizer:", recognizer.name)
    except AlreadyExists:
        print("Recognizer already exists:", recognizer_name)
        recognizer = client.get_recognizer(name=recognizer_name)

    return recognizer

# Replace with your project-specific project ID
project_id = "groovy-age-420314"
recognizer_id = "thothica-test123"  # You can define a recognizer ID here
recognizer_name = f"projects/{project_id}/locations/global/recognizers/{recognizer_id}"

# Create the recognizer if it doesn't exist
create_recognizer_if_not_exists(project_id, recognizer_id)

audio_path = "/Users/ashwintyagi/Desktop/POCs/POC-5/audio/Inaugural Address⧸Shri Rajnesh Singh⧸MHI GovtofIndia⧸How is EV Driving India’s GreenMobility Mission.mp3"
transcript = transcribe_audio_file(audio_path, recognizer_name)

print("Full Transcript:")
print(transcript)






















# from pydub import AudioSegment
# import os
# import math
# from google.cloud import speech_v2 as speech
# from google.cloud.speech_v2.types import cloud_speech
# import io
# import tempfile

# # Set up your Google Cloud credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "GOOGLE_APPLICATION_CREDENTIALS_JSON.json"

# def split_audio(audio_path, chunk_length_ms):
#     audio = AudioSegment.from_file(audio_path, format="mp3")
#     audio_chunks = []
#     total_length = len(audio)
#     num_chunks = math.ceil(total_length / chunk_length_ms)

#     for i in range(num_chunks):
#         start = i * chunk_length_ms
#         end = min(start + chunk_length_ms, total_length)
#         chunk = audio[start:end]
#         audio_chunks.append(chunk)

#     return audio_chunks

# def transcribe_chunk_v2(chunk, recognizer_name, language_code="en-US"):
#     client = speech.SpeechClient()
#     # Export the chunk to a temporary file
#     with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio_file:
#         chunk.export(temp_audio_file.name, format="wav")
#         temp_audio_file.seek(0)
        
#         config = cloud_speech.RecognitionConfig(
#             auto_decoding_config=cloud_speech.AutoDetectDecodingConfig(),
#             language_codes=[language_code],
#             model="long",
#         )

#         file_metadata = cloud_speech.BatchRecognizeFileMetadata(uri=f"file://{temp_audio_file.name}")

#         request = cloud_speech.BatchRecognizeRequest(
#             recognizer=recognizer_name,
#             config=config,
#             files=[file_metadata],
#             recognition_output_config=cloud_speech.RecognitionOutputConfig(
#                 inline_response_config=cloud_speech.InlineOutputConfig(),
#             ),
#         )

#         operation = client.batch_recognize(request=request)

#         print("Waiting for operation to complete...")
#         response = operation.result(timeout=120)

#         transcripts = [result.alternatives[0].transcript for result in response.results[0].transcript.results]
#         return " ".join(transcripts)

# def transcribe_audio_file(audio_path, recognizer_name, chunk_length_ms=60 * 1000):
#     chunks = split_audio(audio_path, chunk_length_ms)
#     full_transcript = ""
    
#     for i, chunk in enumerate(chunks):
#         print(f"Processing chunk {i + 1}/{len(chunks)}...")
#         transcript = transcribe_chunk_v2(chunk, recognizer_name)
#         full_transcript += transcript + " "

#     return full_transcript

# # Replace with your project-specific recognizer name
# recognizer_name = "projects/YOUR_PROJECT_ID/locations/global/recognizers/YOUR_RECOGNIZER_ID"

# audio_path = "/Users/ashwintyagi/Desktop/POCs/POC-5/Inaugural Address⧸Shri Rajnesh Singh⧸MHI GovtofIndia⧸How is EV Driving India’s GreenMobility Mission.mp3"
# transcript = transcribe_audio_file(audio_path, recognizer_name)

# print("Full Transcript:")
# print(transcript)













# from pydub import AudioSegment
# import os
# import math
# from google.cloud import speech_v1p1beta1 as speech
# import io

# # Set up your Google Cloud credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "GOOGLE_APPLICATION_CREDENTIALS_JSON.json"

# def split_audio(audio_path, chunk_length_ms):
#     audio = AudioSegment.from_file(audio_path, format="mp3")
#     audio_chunks = []
#     total_length = len(audio)
#     num_chunks = math.ceil(total_length / chunk_length_ms)

#     for i in range(num_chunks):
#         start = i * chunk_length_ms
#         end = min(start + chunk_length_ms, total_length)
#         chunk = audio[start:end]
#         audio_chunks.append(chunk)

#     return audio_chunks

# def transcribe_chunk(chunk, sample_rate_hertz=44100, language_code="en-US"):
#     audio_content = chunk.export(format="mp3").read()
#     audio = speech.RecognitionAudio(content=audio_content)
#     config = speech.RecognitionConfig(
#         encoding=speech.RecognitionConfig.AudioEncoding.MP3,
#         sample_rate_hertz=sample_rate_hertz,
#         language_code=language_code,
#     )

#     response = client.recognize(config=config, audio=audio)
#     transcripts = [result.alternatives[0].transcript for result in response.results]
#     return " ".join(transcripts)

# client = speech.SpeechClient()

# audio_path = "/Users/ashwintyagi/Desktop/POCs/POC-5/Inaugural Address⧸Shri Rajnesh Singh⧸MHI GovtofIndia⧸How is EV Driving India’s GreenMobility Mission.mp3"
# chunk_length_ms = 60 * 1000  # 60 seconds

# chunks = split_audio(audio_path, chunk_length_ms)

# full_transcript = ""
# for i, chunk in enumerate(chunks):
#     print(f"Processing chunk {i + 1}/{len(chunks)}...")
#     transcript = transcribe_chunk(chunk)
#     full_transcript += transcript + " "

# print("Full Transcript:")
# print(full_transcript)
