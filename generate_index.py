import csv

def generate_index():
    csv_file = 'data.csv'
    video_urls = []

    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            video_urls.append(row[0])

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
        iframe {
            width: 100%;
            height: 100vh;
            scroll-snap-align: start;
            border: none;
        }
    </style>
</head>
<body>
    <div id="video-container">""")

        for url in video_urls:
            embed_url = f"https://twitframe.com/show?url={url}"
            f.write(f"""
        <iframe src="{embed_url}" allowfullscreen></iframe>""")

        f.write("""
    </div>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const videoContainer = document.getElementById("video-container");
            const iframes = videoContainer.getElementsByTagName("iframe");

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
                let closestIframe = null;
                let closestDistance = Infinity;

                Array.from(iframes).forEach(iframe => {
                    const rect = iframe.getBoundingClientRect();
                    const distance = Math.abs(rect.top);

                    if (distance < closestDistance) {
                        closestIframe = iframe;
                        closestDistance = distance;
                    }
                });

                if (closestIframe) {
                    if (startY > endY) {
                        // Scroll down
                        const nextIframe = closestIframe.nextElementSibling;
                        if (nextIframe) {
                            nextIframe.scrollIntoView({ block: 'start' });
                        }
                    } else {
                        // Scroll up
                        const previousIframe = closestIframe.previousElementSibling;
                        if (previousIframe) {
                            previousIframe.scrollIntoView({ block: 'start' });
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
