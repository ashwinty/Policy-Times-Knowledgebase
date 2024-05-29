import os
import yt_dlp as youtube_dl

# Function to download audio from YouTube videos in a playlist
def download_audio_from_playlist(playlist_url, output_directory):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'flac',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s'),
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

# Main function
if __name__ == "__main__":
    playlist_url = "https://www.youtube.com/playlist?list=PLgfecf_dP7vUmS5dR9lvJFKDzmC3pHjAM"  # Replace with your YouTube playlist URL
    output_directory = "downloaded_audio"  # Directory where audio files will be saved

    # Ensure output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Download audio from all videos in the playlist
    download_audio_from_playlist(playlist_url, output_directory)
