document.addEventListener('DOMContentLoaded', function() {
    fetch('data.csv')
        .then(response => response.text())
        .then(text => {
            const lines = text.split('\n').filter(line => line.trim() !== '');
            const contentDiv = document.getElementById('content');

            // Reverse the lines to display the newest first
            lines.reverse();

            lines.forEach(line => {
                const [type, url] = line.split(',');
                const postDiv = document.createElement('div');
                postDiv.className = 'post';

                if (type === 'twitter') {
                    const tweetEmbed = document.createElement('blockquote');
                    tweetEmbed.className = 'twitter-tweet';
                    tweetEmbed.setAttribute('data-media-max-width', '560');
                    const tweetContent = document.createElement('p');
                    const tweetLink = document.createElement('a');
                    tweetLink.href = url.trim();
                    tweetContent.appendChild(tweetLink);
                    tweetEmbed.appendChild(tweetContent);

                    // Adding the script tag for Twitter widgets.js
                    const script = document.createElement('script');
                    script.src = 'https://platform.twitter.com/widgets.js';
                    script.async = true;
                    script.charset = 'utf-8';

                    postDiv.appendChild(tweetEmbed);
                    contentDiv.appendChild(postDiv);
                    document.body.appendChild(script);
                }
            });

            setBackground();  // Call setBackground function to set video background
        });
});

function setBackground() {
    const now = new Date();
    const hours = now.getHours();
    const video = document.getElementById('video');

    if (hours >= 6 && hours < 12) {
        video.src = 'https://www.pexels.com/video/waves-during-sunset-854830/';
    } else if (hours >= 12 && hours < 18) {
        video.src = 'https://www.pexels.com/video/waves-during-daytime-854831/';
    } else {
        video.src = 'https://www.videezy.com/free-video/sunset-beach';
    }

    playVideoOnView();
}

function playVideoOnView() {
    const video = document.getElementById('video');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                video.play();
            } else {
                video.pause();
            }
        });
    });

    observer.observe(video);
}
