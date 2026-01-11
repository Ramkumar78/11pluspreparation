import os
import requests
import time
import random
from comprehension_seed import COMPREHENSION_LIST
from scraper import get_cartoon_image
import re

# Path to store images relative to this script
IMAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'public', 'images', 'comprehension')

def sanitize_filename(title):
    # Remove special chars and replace spaces with underscores
    s = re.sub(r'[^\w\s-]', '', title).strip().lower()
    return re.sub(r'[-\s]+', '_', s)

def download_comprehension_images():
    if not os.path.exists(IMAGE_DIR):
        print(f"Creating directory: {IMAGE_DIR}", flush=True)
        os.makedirs(IMAGE_DIR)

    print(f"Downloading images for {len(COMPREHENSION_LIST)} comprehension passages...", flush=True)

    # Session for connection pooling + User Agent
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

    for i, item in enumerate(COMPREHENSION_LIST):
        title = item['title']
        prompt = item.get('image_prompt', title) # Fallback to title if no prompt
        content_snippet = item['content'][:50]

        filename = f"{sanitize_filename(title)}.jpg"
        filepath = os.path.join(IMAGE_DIR, filename)

        if os.path.exists(filepath):
            # Check for non-empty
            if os.path.getsize(filepath) > 0:
                print(f"[{i+1}/{len(COMPREHENSION_LIST)}] {title}: Exists. Skipping.", flush=True)
                continue

        print(f"[{i+1}/{len(COMPREHENSION_LIST)}] {title}: Downloading...", flush=True)

        # Use get_cartoon_image but we might need to tweak it or just use similar logic
        # get_cartoon_image calls DDG or Pollinations.
        # Since we have a specific prompt, let's try to use that directly if possible or adapt get_cartoon_image.
        # But get_cartoon_image constructs the query.
        # Let's import generate_pollinations_image directly from scraper if possible or reimplement a simple version here.

        from scraper import generate_pollinations_image
        import urllib.parse

        # Use Pollinations directly with the custom prompt for best results matching the "cartoon" requirement
        # prompt already contains "cartoon style" etc.
        encoded_query = urllib.parse.quote(prompt)
        seed = random.randint(1, 1000000)
        url = f"https://image.pollinations.ai/prompt/{encoded_query}?nologo=true&seed={seed}"

        max_retries = 5
        success = False

        for attempt in range(max_retries):
            try:
                response = session.get(url, timeout=60)

                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"  -> SAVED {filename}", flush=True)
                    success = True
                    break
                elif response.status_code == 429:
                    wait_time = (2 ** attempt) + 5
                    print(f"  -> Rate Limited (429). Waiting {wait_time}s...", flush=True)
                    time.sleep(wait_time)
                else:
                    print(f"  -> Failed: {response.status_code}", flush=True)
                    time.sleep(2)
            except Exception as e:
                print(f"  -> Error: {e}", flush=True)
                time.sleep(2)

        if not success:
            print(f"  -> GAVE UP on {title}", flush=True)

        # Polite delay
        time.sleep(1)

if __name__ == "__main__":
    download_comprehension_images()
