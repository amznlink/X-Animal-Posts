import requests
from github import Github
import os

# Fetch the list of URLs from a file in the GitHub repository
def get_file_content(repo_name, file_path, github_token):
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    file_content = repo.get_contents(file_path)
    return file_content.decoded_content.decode('utf-8')

# Fetch the embed code for each URL using Twitter's oEmbed API
def fetch_embed_code(tweet_url):
    api_url = f"https://publish.twitter.com/oembed?url={tweet_url}&format=json"
    response = requests.get(api_url)
    return response.json()['html']

# Generate the HTML file with embed codes
def generate_html(embed_codes):
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Animals</title>
        <style>
            body, html {
                height: 100%;
                margin: 0;
            }
            .embed-container {
                display: block;
                width: 100%;
                border: none;
                position: relative;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
    """

    for code in embed_codes:
        html_content += f'<div class="embed-container">{code}</div>\n'

    html_content += """
    <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
    </body>
    </html>
    """
    return html_content

# Main function
def main():
    github_token = os.getenv('GITHUB_TOKEN')
    repo_name = os.getenv('REPO_NAME')
    file_path = os.getenv('FILE_PATH')

    # Get the list of URLs
    file_content = get_file_content(repo_name, file_path, github_token)
    urls = file_content.strip().split('\n')

    # Fetch embed codes
    embed_codes = [fetch_embed_code(url) for url in urls if url.strip()]

    # Generate HTML
    html_content = generate_html(embed_codes)
    
    # Write HTML to file
    with open('index.html', 'w') as file:
        file.write(html_content)

if __name__ == "__main__":
    main()
