from instagrapi import Client
import os
import requests
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Load environment variables from .env file
load_dotenv()

def download_reels(username, password, collection_name):
    client = Client()
    client.login(username,password)
    
    # Get collection medias by name
    collection_medias = client.collection_medias_by_name(collection_name)
    
    video_clips = []
    media_ids = []
    for media in collection_medias:
        media_info = client.media_info(media.id)
        
        if(media_info.media_type == 2):
            video_url = media_info.video_url
            video_filename = download_video(video_url, f"{media.id}.mp4")
            print(f"Downloaded {video_filename}")
            video_clip = VideoFileClip(video_filename)
            video_clips.append(video_clip)
            media_ids.append(media.id)
        
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
    collection_name = input("Please type your collection name: ")

    if not (instagram_username and instagram_password):
        print("Error: Instagram credentials not found in .env file.")
        return


    download_reels(instagram_username, instagram_password, collection_name)


if __name__ == "__main__":
    main()
