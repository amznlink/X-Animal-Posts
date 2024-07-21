document.addEventListener('DOMContentLoaded', function() {
    fetch('data.csv')
        .then(response => response.text())
        .then(text => {
            const lines = text.split('\\n').filter(line => line.trim() !== '');
            const videoContainer = document.getElementById('video-container');

            lines.forEach(line => {
                const [type, url] = line.split(',');
                if (type === 'video') {
                    fetch(`https://noembed.com/embed?url=${url.trim()}`)
                        .then(response => response.json())
                        .then(data => {
                            const videoDiv = document.createElement('div');
                            videoDiv.className = 'post';
                            const tempDiv = document.createElement('div');
                            tempDiv.innerHTML = data.html;
                            const iframe = tempDiv.querySelector('iframe');
                            videoDiv.appendChild(iframe);
                            videoContainer.appendChild(videoDiv);
                        });
                }
            });
        });
});
