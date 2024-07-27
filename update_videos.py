import os
import json

def update_videos_json():
    videos_folder = 'videos'
    video_extensions = ('.mp4', '.mov', '.avi', '.mkv')
    video_files = [f for f in os.listdir(videos_folder) if f.endswith(video_extensions)]

    videos_json_path = os.path.join(videos_folder, 'videos.json')
    with open(videos_json_path, 'w') as json_file:
        json.dump(video_files, json_file, indent=4)

if __name__ == '__main__':
    update_videos_json()
    print("videos.json has been updated with the latest video files.")
