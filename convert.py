from pydub import AudioSegment
import os

def convert_flac_to_mp3(flac_folder, mp3_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(mp3_folder):
        os.makedirs(mp3_folder)

    # Iterate through each file in the FLAC folder
    for filename in os.listdir(flac_folder):
        if filename.endswith(".flac"):
            flac_file = os.path.join(flac_folder, filename)
            mp3_file = os.path.join(mp3_folder, filename[:-5] + ".mp3")  # Change extension to .mp3
            
            # Load the FLAC file
            audio = AudioSegment.from_file(flac_file, format="flac")
            
            # Export as MP3
            audio.export(mp3_file, format="mp3")

# Example usage
if __name__ == "__main__":
    flac_folder = "downloaded_audio"  # Replace with the path to your folder containing FLAC files
    mp3_folder = "audio"         # Name of the folder where MP3 files will be saved

    convert_flac_to_mp3(flac_folder, mp3_folder)
    print("Conversion completed successfully!")
