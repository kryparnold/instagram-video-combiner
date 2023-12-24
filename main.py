from instagrapi import Client
import json
import os
import requests
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Load environment variables from .env file
load_dotenv()

def download_reels(username, password, reels_urls):
    client = Client()
    client.login(username, password)

    video_clips = []
    media_ids = []  # Keep track of media IDs

    for url in reels_urls:
        media_id = client.media_pk_from_url(url)
        media_info = client.media_info(media_id)
        
        if media_info.media_type == 2:  # 2 represents video media type
            video_url = media_info.video_url
            video_filename = download_video(video_url, f"{media_id}.mp4")
            print(f"Downloaded {video_filename}")
            video_clip = VideoFileClip(video_filename)
            video_clips.append(video_clip)
            media_ids.append(media_id)
            
    if video_clips:
        # Trim a small portion (1 second) from the end of each video to avoid repetition
        trimmed_clips = [clip.subclip(0, clip.duration - 0.25) for clip in video_clips]
        final_clip = concatenate_videoclips(trimmed_clips, method="compose")
        final_filename = "combined_video.mp4"
        final_clip.write_videofile(final_filename, codec="libx264", fps=24)
        print(f"Combined videos saved as {final_filename}")

        # Close the video clips to release resources
        for clip in video_clips:
            clip.close()

        # Delete downloaded videos
        delete_downloaded_videos(media_ids)

    # Close the client to clean up resources
    client.logout()

def download_video(url, filename):
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    return filename

def delete_downloaded_videos(media_ids):
    for media_id in media_ids:
        video_filename = f"{media_id}.mp4"
        if os.path.exists(video_filename):
            os.remove(video_filename)
            print(f"Deleted {video_filename}")

def main():
    instagram_username = os.getenv('INSTAGRAM_USERNAME')
    instagram_password = os.getenv('INSTAGRAM_PASSWORD')

    if not (instagram_username and instagram_password):
        print("Error: Instagram credentials not found in .env file.")
        return

    try:
        with open('reels.json', 'r') as file:
            reels_data = json.load(file)
            reels_urls = reels_data.get('urls', [])
            download_reels(instagram_username, instagram_password, reels_urls)
    except FileNotFoundError:
        print("Error: reels.json not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON in reels.json file.")

if __name__ == "__main__":
    main()
