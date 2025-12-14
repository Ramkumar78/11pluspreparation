import urllib.parse

def get_cartoon_image(word):
    """
    Generates a 'cartoon' or 'illustration' of the word using pollinations.ai.
    """
    # Safe search query for kids
    query = f"cartoon illustration of {word}, kid friendly, vibrant colors"
    encoded_query = urllib.parse.quote(query)
    # nologo=true removes the watermark
    url = f"https://image.pollinations.ai/prompt/{encoded_query}?nologo=true"

    return url
