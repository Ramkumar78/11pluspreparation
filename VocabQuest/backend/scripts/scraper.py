from duckduckgo_search import DDGS
import time
import random
import urllib.parse

def get_cartoon_image(word, definition, synonym=""):
    """
    Finds a real image using DuckDuckGo Search (High quality, relevant, fast).
    """
    # Negative keywords to avoid text, diagrams, and unsafe content
    # We explicitly exclude the word itself to prevent it from appearing in the image
    # Negative keywords to avoid text, diagrams, and unsafe content
    # We explicitly exclude the word itself to prevent it from appearing in the image
    negatives = f"-{word} -text -word -label -diagram -chart -screenshot -cartoon -drawing -sketch -textbook -quote -sign -writing -logo -educational -grammar -slide -definition -dictionary -meaning"
    
    # Words that are known to produce text-heavy results or are abstract -> Force Generation
    FORCE_GENERATE_WORDS = ["succinct", "evade", "abide", "retract", "abstract", "inference"]
    
    if word.lower() in FORCE_GENERATE_WORDS:
        print(f"  (Forcing generation for '{word}')", flush=True)
        # Fallback logic handles generation
        return generate_pollinations_image(word, definition)

    queries = [
        f"{word} {synonym} realistic photo {negatives}",          # Best: Word + Synonym
        f"{word} {definition} realistic photo {negatives}",       # Context: Word + Def
        f"{word} realistic photo {negatives}"                     # Fallback: Just Word
    ]
    
    for query in queries:
        try:
            with DDGS() as ddgs:
                # Search for 1 image
                results = list(ddgs.images(
                    keywords=query,
                    max_results=1,
                    safesearch='on', # Safety first for kids app
                    type_image='photo'
                ))
                if results and 'image' in results[0]:
                    print(f"  (Found via: '{query}')", flush=True)
                    return results[0]['image']
        except Exception as e:
            print(f"  (DDG Error on '{query}': {e})", flush=True)
            time.sleep(1)

    # Fallback: Use Pollinations.ai with definition (relevant, not a placeholder)
    print("  (Fallback to Pollinations.ai)", flush=True)
    return generate_pollinations_image(word, definition)

def generate_pollinations_image(word, definition):
    """
    Generates a URL using Pollinations.ai with the word definition.
    """
    prompt = f"photographic image representing '{word}': {definition}. generic, high quality, 8k, realistic, cinematic lighting"
    encoded_query = urllib.parse.quote(prompt)
    seed = random.randint(1, 1000000)
    return f"https://image.pollinations.ai/prompt/{encoded_query}?nologo=true&seed={seed}"

