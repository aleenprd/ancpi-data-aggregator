import requests
import re

url = "https://www.ancpi.ro/wp-content/plugins/download-attachments/includes/download.php?id=17882"

response = requests.get(url)

if response.status_code == 200:
    content_disposition = response.headers.get("Content-Disposition")
    if content_disposition:
        # Try to extract the filename from the header
        filename_match = re.search('filename="(.+)"', content_disposition)
        if filename_match:
            filename = filename_match.group(1)
        else:
            filename = "downloaded_file.xlsx"
    else:
        filename = "downloaded_file.xlsx"  # fallback

    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"File successfully downloaded as '{filename}'")
else:
    print(f"Failed to download file. Status code: {response.status_code}")
