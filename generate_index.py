import csv
import requests
from bs4 import BeautifulSoup

def extract_media_url(tweet_url):
    response = requests.get(tweet_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Try to extract video URL
    video_tag = soup.find('meta', {'property': 'og:video:url'})
    if video_tag and video_tag.get('content'):
        return video_tag['content']
    
    # Try to extract image URL
    image_tag = soup.find('meta', {'property': 'og:image'})
    if image_tag and image_tag.get('content'):
        return image_tag['content']
    
    return None

def generate_index():
    csv_file = 'data.csv'
    media_urls = []

    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Ensure the row is not empty
                media_url = extract_media_url(row[0])
                if media_url:
                    media_urls.append(media_url)

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
        #media-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            scroll-snap-type: y mandatory;
        }
        .media {
            width: 100%;
            height: 100vh;
            scroll-snap-align: start;
            border: none;
        }
    </style>
</head>
<body>
    <div id="media-container">""")

        for url in media_urls:
            if 'video' in url or url.endswith('.mp4'):
                f.write(f"""
        <video class="media" controls>
            <source src="{url}" type="video/mp4">
            Your browser does not support the video tag.
        </video>""")
            else:
                f.write(f"""
        <img class="media" src="{url}" alt="Image">""")

        f.write("""
    </div>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const mediaContainer = document.getElementById("media-container");
            const mediaElements = mediaContainer.getElementsByClassName("media");

            let startY = 0;
            let endY = 0;

            document.addEventListener('touchstart', function(event) {
                startY = event.touches[0].clientY;
            });

            document.addEventListener('touchend', function(event) {
                endY = event.changedTouches[0].clientY;
                handleTouchScroll();
            });

            function handleTouchScroll() {
                let closestMedia = null;
                let closestDistance = Infinity;

                Array.from(mediaElements).forEach(media => {
                    const rect = media.getBoundingClientRect();
                    const distance = Math.abs(rect.top);

                    if (distance < closestDistance) {
                        closestMedia = media;
                        closestDistance = distance;
                    }
                });

                if (closestMedia) {
                    if (startY > endY) {
                        // Scroll down
                        const nextMedia = closestMedia.nextElementSibling;
                        if (nextMedia) {
                            nextMedia.scrollIntoView({ block: 'start' });
                        }
                    } else {
                        // Scroll up
                        const previousMedia = closestMedia.previousElementSibling;
                        if (previousMedia) {
                            previousMedia.scrollIntoView({ block: 'start' });
                        }
                    }
                }
            }
        });

        document.documentElement.style.scrollBehavior = 'auto';
    </script>
</body>
</html>""")

if __name__ == '__main__':
    generate_index()
