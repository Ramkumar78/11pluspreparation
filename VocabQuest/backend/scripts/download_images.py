import os
import sys
import requests
import time
import random

# Add parent directory to path to allow importing seed_list
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seed_list import WORD_LIST
import scraper

# Path to store images relative to this script
IMAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'frontend', 'public', 'images')

def download_images():
    if not os.path.exists(IMAGE_DIR):
        print(f"Creating directory: {IMAGE_DIR}", flush=True)
        os.makedirs(IMAGE_DIR)

    print(f"Downloading images for {len(WORD_LIST)} words (SEQUENTIAL)...", flush=True)

    # Session for connection pooling + User Agent
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

    for i, item in enumerate(WORD_LIST):
        word = item['text']
        definition = item.get('def', '') # Get definition
        synonym = item.get('synonym', '')
        filename = f"{word}.jpg"
        filepath = os.path.join(IMAGE_DIR, filename)

        if os.path.exists(filepath):
            # Check for non-empty
            if os.path.getsize(filepath) > 0:
                print(f"[{i+1}/{len(WORD_LIST)}] {word}: Exists. Skipping.", flush=True)
                continue

        print(f"[{i+1}/{len(WORD_LIST)}] {word}: Downloading...", flush=True)
        
        url = scraper.get_cartoon_image(word, definition, synonym)

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
            print(f"  -> GAVE UP on {word}", flush=True)
        
        # Polite delay between words
        time.sleep(1)

if __name__ == "__main__":
    download_images()
