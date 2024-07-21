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
                } else if (type === 'youtube') {
                    const iframe = document.createElement('iframe');
                    iframe.width = '560';
                    iframe.height = '315';
                    iframe.src = `https://www.youtube.com/embed/${url.trim().split('v=')[1]}`;
                    iframe.frameBorder = '0';
                    iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
                    iframe.allowFullscreen = true;
                    postDiv.appendChild(iframe);
                    contentDiv.appendChild(postDiv);
                }
            });
        });
});
