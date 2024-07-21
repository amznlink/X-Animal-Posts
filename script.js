document.addEventListener('DOMContentLoaded', function() {
    fetch('data.csv')
        .then(response => response.text())
        .then(text => {
            const lines = text.split('\n').filter(line => line.trim() !== '');
            const videoContainer = document.getElementById('video-container');

            lines.forEach(line => {
                const tweetDiv = document.createElement('div');
                tweetDiv.className = 'post';
                tweetDiv.innerHTML = line.trim();
                videoContainer.appendChild(tweetDiv);
            });

            // Load Twitter widgets script
            const script = document.createElement('script');
            script.src = 'https://platform.twitter.com/widgets.js';
            script.async = true;
            script.charset = 'utf-8';
            document.body.appendChild(script);
        });
});
