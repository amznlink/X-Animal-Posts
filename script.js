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

            // Adjust tweet dimensions after loading
            setTimeout(() => {
                $('.twitter-tweet').each(function() {
                    const iframe = $(this).find('iframe');
                    if (iframe.length) {
                        const doc = iframe[0].contentDocument || iframe[0].contentWindow.document;
                        $(doc).find('head').append($('#twitter-style'));
                    }
                });
            }, 2000);

            // Set up IntersectionObserver to handle autoplay and pause
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    const iframe = entry.target.querySelector('iframe');
                    if (iframe) {
                        const src = iframe.getAttribute('src');
                        const video = iframe.contentWindow.document.querySelector('video');
                        if (entry.isIntersecting) {
                            iframe.setAttribute('src', src + (src.includes('?') ? '&' : '?') + 'autoplay=1');
                            if (video) video.play();
                        } else {
                            iframe.setAttribute('src', src.replace('&autoplay=1', '').replace('?autoplay=1', ''));
                            if (video) video.pause();
                        }
                    }
                });
            }, { threshold: 0.75 });

            document.querySelectorAll('.post').forEach(post => {
                observer.observe(post);
            });
        });
});
