import os
import requests
import time
import random
from seed_list import WORD_LIST
from scraper import get_cartoon_image

# Path to store images relative to this script
IMAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'public', 'images')

def download_images():
    if not os.path.exists(IMAGE_DIR):
        print(f"Creating directory: {IMAGE_DIR}", flush=True)
        os.makedirs(IMAGE_DIR)

    print(f"Downloading images for {len(WORD_LIST)} words...", flush=True)

    for i, item in enumerate(WORD_LIST):
        word = item['text']
        filename = f"{word}.jpg"
        filepath = os.path.join(IMAGE_DIR, filename)

        if os.path.exists(filepath):
            print(f"[{i+1}/{len(WORD_LIST)}] {word}: Already exists. Skipping.", flush=True)
            continue

        print(f"[{i+1}/{len(WORD_LIST)}] {word}: Downloading...", flush=True)

        max_retries = 3
        for attempt in range(max_retries):
            try:
                url = get_cartoon_image(word)
                # Increased timeout to 60s as generation takes time
                response = requests.get(url, timeout=60)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"  Saved to {filename}", flush=True)
                    break
                elif response.status_code == 429:
                    wait_time = (2 ** attempt) + random.uniform(1, 3)
                    print(f"  Rate limited (429). Retrying in {wait_time:.2f}s...", flush=True)
                    time.sleep(wait_time)
                else:
                    print(f"  Failed with status code: {response.status_code}. Retrying...", flush=True)
                    time.sleep(2)
            except Exception as e:
                print(f"  Error downloading {word} (Attempt {attempt+1}): {e}", flush=True)
                time.sleep(2)
        else:
             print(f"  Failed to download {word} after {max_retries} attempts.", flush=True)

        # Small delay to avoid hammering
        time.sleep(1)

if __name__ == "__main__":
    download_images()
