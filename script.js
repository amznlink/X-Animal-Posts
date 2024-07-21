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
        });
});
