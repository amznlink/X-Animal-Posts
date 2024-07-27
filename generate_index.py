import os

def generate_index():
    videos_folder = 'videos'
    video_extensions = ('.mp4', '.mov', '.avi', '.mkv')
    video_files = [f for f in os.listdir(videos_folder) if f.endswith(video_extensions)]
    
    with open('index.html', 'w') as f:
        f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Animal Videos</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow-x: hidden;
            font-family: Arial, sans-serif;
            scroll-snap-type: y mandatory;
            height: 100vh;
            overflow-y: scroll;
        }
        #video-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            scroll-snap-type: y mandatory;
        }
        video {
            width: 100%;
            height: 100vh;
            object-fit: cover;
            scroll-snap-align: start;
            border: none;
        }
    </style>
</head>
<body>
    <div id="video-container">""")

        for video in video_files:
            f.write(f"""
        <video src="videos/{video}" controls></video>""")

        f.write("""
    </div>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const videoContainer = document.getElementById("video-container");
            const videos = videoContainer.getElementsByTagName("video");

            Array.from(videos).forEach(videoElement => {
                videoElement.addEventListener('play', () => {
                    Array.from(videos).forEach(v => {
                        if (v !== videoElement) {
                            v.pause();
                        }
                    });
                });
            });
        });

        window.addEventListener('wheel', function(event) {
            if (event.deltaY > 0) {
                scrollToNext();
            } else if (event.deltaY < 0) {
                scrollToPrevious();
            }
        });

        function scrollToNext() {
            const currentVideo = document.querySelector('video[autoplay]');
            if (currentVideo && currentVideo.nextElementSibling) {
                currentVideo.nextElementSibling.scrollIntoView({ behavior: 'auto' });
            } else if (!currentVideo && videos.length > 0) {
                videos[0].scrollIntoView({ behavior: 'auto' });
            }
        }

        function scrollToPrevious() {
            const currentVideo = document.querySelector('video[autoplay]');
            if (currentVideo && currentVideo.previousElementSibling) {
                currentVideo.previousElementSibling.scrollIntoView({ behavior: 'auto' });
            }
        }

        const videos = document.querySelectorAll('video');
        videos.forEach(video => {
            video.addEventListener('play', () => {
                videos.forEach(v => v.removeAttribute('autoplay'));
                video.setAttribute('autoplay', 'true');
            });
        });
    </script>
</body>
</html>""")

if __name__ == '__main__':
    generate_index()
