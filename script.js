document.addEventListener('DOMContentLoaded', function() {
    fetch('data.csv')
        .then(response => response.text())
        .then(text => {
            const lines = text.split('\n').filter(line => line.trim() !== '');
            const tweetContainer = document.getElementById('tweet-container');

            lines.forEach(line => {
                const tweetDiv = document.createElement('div');
                tweetDiv.className = 'post';
                tweetDiv.innerHTML = line.trim();
                tweetContainer.appendChild(tweetDiv);
            });

            // Load Twitter widgets script
            const script = document.createElement('script');
            script.src = 'https://platform.twitter.com/widgets.js';
            script.async = true;
            script.charset = 'utf-8';
            document.body.appendChild(script);

            // Set up IntersectionObserver to handle autoplay and pause
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    const iframe = entry.target.querySelector('iframe');
                    const src = iframe ? iframe.getAttribute('src') : '';
                    if (entry.isIntersecting && iframe) {
                        iframe.setAttribute('src', src + (src.includes('?') ? '&' : '?') + 'autoplay=1');
                    } else if (iframe) {
                        iframe.setAttribute('src', src.replace('&autoplay=1', '').replace('?autoplay=1', ''));
                    }
                });
            }, { threshold: 0.75 });

            document.querySelectorAll('.post').forEach(post => {
                observer.observe(post);
            });

            // Adjust tweet dimensions after loading
            setTimeout(() => {
                document.querySelectorAll('.twitter-tweet').forEach(tweet => {
                    const shadowRoot = tweet.shadowRoot;
                    if (shadowRoot) {
                        const embeddedTweet = shadowRoot.querySelector('.EmbeddedTweet');
                        if (embeddedTweet) {
                            embeddedTweet.style.width = '99%';
                            embeddedTweet.style.maxWidth = '100%';
                        }
                    }
                });
            }, 2000);
        });
});
