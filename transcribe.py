# Import necessary libraries
import os
from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
import logging
import time

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up your Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "GOOGLE_APPLICATION_CREDENTIALS_JSON.json"

# Function to convert audio to WAV format
def convert_to_wav(audio_file_path):
    try:
        audio = AudioSegment.from_file(audio_file_path)
        wav_file_path = os.path.splitext(audio_file_path)[0] + ".wav"
        audio.export(wav_file_path, format="wav")
        return wav_file_path
    except Exception as e:
        logging.error(f"Error converting audio to WAV: {e}")
        return None

# Function to split audio into smaller chunks ensuring each chunk is below 10MB
def split_audio(audio_file_path, chunk_length_ms=30000):
    audio = AudioSegment.from_file(audio_file_path, format="wav")
    chunks = []
    start = 0
    while start < len(audio):
        end = min(start + chunk_length_ms, len(audio))
        chunk = audio[start:end]
        chunks.append(chunk)
        start = end
    return chunks

# Function to transcribe a chunk of audio using Google Cloud Speech-to-Text
def transcribe_chunk(audio_chunk, retry_count=3):
    client = speech.SpeechClient()

    audio_content = audio_chunk.raw_data
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,  # Reduced sample rate to reduce payload size
        language_code="en-US",
    )

    for attempt in range(retry_count):
        try:
            operation = client.long_running_recognize(request={"config": config, "audio": audio})
            logging.info("Waiting for operation to complete...")
            response = operation.result(timeout=600)  # Adjust timeout as needed

            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript + "\n"
            return transcript
        except Exception as e:
            logging.error(f"Error transcribing chunk: {e}")
            time.sleep(5)  # Wait before retrying
    return ""

# Main function to process all audio files
if __name__ == "__main__":
    audio_directory = "downloaded_audio"  # Directory containing audio files
    transcripts_directory = "transcripts"  # Directory to save transcripts

    # Ensure transcripts directory exists
    if not os.path.exists(transcripts_directory):
        os.makedirs(transcripts_directory)

    # List all audio files in the directory
    audio_files = [f for f in os.listdir(audio_directory) if f.endswith('.mp3')]

    for audio_file in audio_files:
        source_file_path = os.path.join(audio_directory, audio_file)

        # Convert audio file to WAV format
        wav_file_path = convert_to_wav(source_file_path)
        if wav_file_path:
            logging.info(f"Converted {audio_file} to WAV format: {wav_file_path}")

            # Split audio file into smaller chunks
            chunks = split_audio(wav_file_path)

            # Transcribe each chunk and combine the results
            full_transcript = ""
            for i, chunk in enumerate(chunks):
                logging.info(f"Transcribing chunk {i + 1} of {len(chunks)} for file {audio_file}...")
                transcript = transcribe_chunk(chunk)
                logging.info(f"Chunk {i + 1} transcript:\n{transcript}")
                full_transcript += transcript

            # Save full transcript to file
            transcript_file_path = os.path.join(transcripts_directory, f"{os.path.splitext(audio_file)[0]}.txt")
            with open(transcript_file_path, "w") as transcript_file:
                transcript_file.write(full_transcript)

            logging.info(f"Transcription for {audio_file} saved to {transcript_file_path}.")
        else:
            logging.error(f"Failed to convert {audio_file} to WAV format.")
