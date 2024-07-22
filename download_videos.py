import csv
import os
import requests
from pathlib import Path
import shutil

# Directory to save downloaded videos
videos_dir = Path("videos")
videos_dir.mkdir(exist_ok=True)

# Read CSV file and download videos
csv_file = "data.csv"
video_urls = []
video_metadata = []

# Read the URLs from the CSV file
with open(csv_file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:
            video_url = row[0]
            video_urls.append(video_url)
            video_filename = videos_dir / f"{video_url.split('/')[-1]}.mp4"
            video_metadata.append((video_filename.name, video_url))
            if not video_filename.exists():
                response = requests.get(video_url, stream=True)
                with open(video_filename, 'wb') as video_file:
                    shutil.copyfileobj(response.raw, video_file)
                del response

# Remove videos not in the CSV
for video_file in videos_dir.iterdir():
    if video_file.name not in [vm[0] for vm in video_metadata]:
        os.remove(video_file)

print(f"Downloaded and verified videos: {video_urls}")

# Save the video metadata to a JSON file
import json
metadata_file = "videos_metadata.json"
with open(metadata_file, 'w') as json_file:
    json.dump(video_metadata, json_file)

print(f"Metadata file '{metadata_file}' generated successfully.")
