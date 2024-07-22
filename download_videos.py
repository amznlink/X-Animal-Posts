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

# Generate HTML to embed videos
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>𝕏 Animal Posts</title>
    <style>
        body, html {
            height: 100%;
            margin: 0;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #000;
            color: white;
            overflow: hidden;
        }

        #video-container {
            position: relative;
            width: 100%;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: black;
        }

        video {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .logo {
            position: absolute;
            top: 10px;
            left: 10px;
            font-size: 24px;
            color: white;
            text-decoration: none;
            z-index: 100;
        }

        .hidden {
            display: none;
        }
    </style>
</head>
<body>
    <div id="video-container">
        <video id="current-video" controls></video>
        <a id="video-logo" class="logo" target="_blank">𝕏</a>
        <div id="loading-indicator" class="hidden">Loading...</div>
    </div>

    <script>
        let currentVideoIndex = 0;
        const videoContainer = document.getElementById('video-container');
        const videoElement = document.getElementById('current-video');
        const videoLogo = document.getElementById('video-logo');
        const loadingIndicator = document.getElementById('loading-indicator');

        const videos = [
"""

for video_file, video_url in video_metadata:
    html_content += f'            {{"file": "videos/{video_file}", "url": "{video_url}"}},\n'

html_content += """
        ];

        function loadVideo() {
            if (loadingIndicator) loadingIndicator.classList.remove('hidden');
            try {
                const currentVideo = videos[currentVideoIndex];
                videoElement.src = currentVideo.file;
                videoElement.load();
                videoElement.play();
                videoLogo.href = currentVideo.url;
            } catch (error) {
                console.error('Error loading video:', error);
            } finally {
                if (loadingIndicator) loadingIndicator.classList.add('hidden');
            }
        }

        function handleSwipe(event) {
            if (event.deltaY > 0) {
                currentVideoIndex = (currentVideoIndex + 1) % videos.length;
            } else {
                currentVideoIndex = (currentVideoIndex - 1 + videos.length) % videos.length;
            }
            loadVideo();
        }

        function handleVideoEnd() {
            currentVideoIndex = (currentVideoIndex + 1) % videos.length;
            loadVideo();
        }

        document.addEventListener('DOMContentLoaded', loadVideo);
        videoContainer.addEventListener('wheel', handleSwipe);
        videoElement.addEventListener('ended', handleVideoEnd);
    </script>
</body>
</html>
"""

# Save the generated HTML
html_filename = "index.html"
with open(html_filename, 'w') as html_file:
    html_file.write(html_content)

print(f"HTML file '{html_filename}' generated successfully.")
