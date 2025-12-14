import requests
from bs4 import BeautifulSoup
import random

def get_cartoon_image(word):
    """
    Scrapes Unsplash for 'cartoon' or 'illustration' of the word.
    """
    # Safe search query for kids
    query = f"{word} cartoon illustration"
    url = f"https://unsplash.com/s/photos/{query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Unsplash specific selectors (may change, but usually reliable for basic scrape)
            images = soup.find_all('img')
            valid_urls = []
            for img in images:
                src = img.get('src', '')
                if 'images.unsplash.com' in src and 'w=1000' in src:
                    valid_urls.append(src)

            if valid_urls:
                return random.choice(valid_urls[:4])
    except Exception as e:
        print(f"Scrape error for {word}: {e}")

    # Fallback image
    return "https://placehold.co/600x400?text=Image+Loading+Error"
