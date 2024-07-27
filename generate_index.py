import csv

def generate_index():
    csv_file = 'data.csv'
    blockquotes_and_scripts = []

    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row:  # Ensure the row is not empty
                blockquotes_and_scripts.append(row[0])

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
        #tweet-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            scroll-snap-type: y mandatory;
        }
        .tweet {
            width: 100%;
            height: 100vh;
            scroll-snap-align: start;
            border: none;
        }
    </style>
</head>
<body>
    <div id="tweet-container">""")

        for blockquote_and_script in blockquotes_and_scripts:
            f.write(f"""
        {blockquote_and_script}""")

        f.write("""
    </div>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const tweetContainer = document.getElementById("tweet-container");
            const tweets = tweetContainer.getElementsByClassName("tweet");

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
                let closestTweet = null;
                let closestDistance = Infinity;

                Array.from(tweets).forEach(tweet => {
                    const rect = tweet.getBoundingClientRect();
                    const distance = Math.abs(rect.top);

                    if (distance < closestDistance) {
                        closestTweet = tweet;
                        closestDistance = distance;
                    }
                });

                if (closestTweet) {
                    if (startY > endY) {
                        // Scroll down
                        const nextTweet = closestTweet.nextElementSibling;
                        if (nextTweet) {
                            nextTweet.scrollIntoView({ block: 'start' });
                        }
                    } else {
                        // Scroll up
                        const previousTweet = closestTweet.previousElementSibling;
                        if (previousTweet) {
                            previousTweet.scrollIntoView({ block: 'start' });
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
