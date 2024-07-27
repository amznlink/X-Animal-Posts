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
                // Add event listener for playing video when in view
                const observer = new IntersectionObserver(entries => {
                    entries.forEach(entry => {
                        if (entry.isIntersecting) {
                            videoElement.play();
                        } else {
                            videoElement.pause();
                        }
                    });
                }, { threshold: 0.75 });
                observer.observe(videoElement);
            });
        });

        window.addEventListener('scroll', function() {
            const videos = document.querySelectorAll('video');
            let closestVideo = null;
            let closestDistance = Infinity;

            videos.forEach(video => {
                const rect = video.getBoundingClientRect();
                const distance = Math.abs(rect.top);

                if (distance < closestDistance) {
                    closestVideo = video;
                    closestDistance = distance;
                }
            });

            if (closestVideo) {
                closestVideo.scrollIntoView({ behavior: 'fast', block: 'start' });
            }
        });

        // Override smooth scrolling duration
        document.documentElement.style.scrollBehavior = 'fast';
        window.addEventListener('scroll', () => {
            clearTimeout(window.scrollTimeout);
            window.scrollTimeout = setTimeout(() => {
                document.documentElement.style.scrollBehavior = 'auto';
            }, 100);
        });
    </script>
</body>
</html>""")

if __name__ == '__main__':
    generate_index()
