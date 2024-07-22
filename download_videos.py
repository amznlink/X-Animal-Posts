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

with open(csv_file, newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:
            video_url = row[0]
            video_urls.append(video_url)
            video_filename = videos_dir / f"{video_url.split('/')[-1]}.mp4"
            if not video_filename.exists():
                response = requests.get(video_url, stream=True)
                with open(video_filename, 'wb') as video_file:
                    shutil.copyfileobj(response.raw, video_file)
                del response

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
            width: 80%;
            height: auto;
            margin-bottom: 20px;
        }

        a {
            color: #1DA1F2;
            text-decoration: none;
            margin-bottom: 40px;
        }

        #loading-indicator {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 24px;
            display: none;
        }
    </style>
</head>
<body>
    <div id="video-container">
        <div id="tweet-container"></div>
        <div id="loading-indicator">Loading...</div>
    </div>

    <script>
        let currentVideoIndex = 0;
        const videos = [
"""

for video_url in video_urls:
    video_filename = f"videos/{video_url.split('/')[-1]}.mp4"
    html_content += f'            {{ url: "{video_filename}", originalUrl: "{video_url}" }},\n'

html_content += """
        ];

        function loadVideo() {
            const loadingIndicator = document.getElementById('loading-indicator');
            const tweetContainer = document.getElementById('tweet-container');

            if (loadingIndicator) loadingIndicator.style.display = 'block';
            tweetContainer.innerHTML = ''; // Clear previous content

            try {
                const currentVideo = videos[currentVideoIndex];
                const videoElement = document.createElement('video');
                videoElement.controls = true;
                videoElement.src = currentVideo.url;
                tweetContainer.appendChild(videoElement);

                const linkElement = document.createElement('a');
                linkElement.href = currentVideo.originalUrl;
                linkElement.target = "_blank";
                linkElement.textContent = "Original URL";
                tweetContainer.appendChild(linkElement);

                currentVideoIndex = (currentVideoIndex + 1) % videos.length; // Cycle through the URLs
            } catch (error) {
                console.error('Error loading video:', error);
            } finally {
                if (loadingIndicator) loadingIndicator.style.display = 'none';
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

        document.addEventListener('DOMContentLoaded', loadVideo);
        document.getElementById('video-container').addEventListener('wheel', handleSwipe);
        document.getElementById('video-container').addEventListener('click', loadVideo);
    </script>
</body>
</html>
"""

# Save the generated HTML
html_filename = "index.html"
with open(html_filename, 'w') as html_file:
    html_file.write(html_content)

print(f"HTML file '{html_filename}' generated successfully.")
