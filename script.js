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
                    const link = document.createElement('a');
                    link.href = url.trim();
                    tweetEmbed.appendChild(link);
                    postDiv.appendChild(tweetEmbed);
                    contentDiv.appendChild(postDiv);
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

            // Load Twitter widgets script
            const script = document.createElement('script');
            script.src = 'https://platform.twitter.com/widgets.js';
            script.async = true;
            document.body.appendChild(script);
        });
});
