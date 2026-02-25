import os
import hashlib

IMAGE_DIR = r"e:\PycharmProjects\11pluspreparation\VocabQuest\frontend\public\images"

count = 0
for filename in os.listdir(IMAGE_DIR):
    if filename.endswith(".jpg"):
        word = filename[:-4] # remove .jpg
        
        # Check if already hashed
        if len(word) == 32 and all(c in '0123456789abcdef' for c in word):
            continue
            
        hashed_word = hashlib.md5(word.encode('utf-8')).hexdigest()
        
        old_path = os.path.join(IMAGE_DIR, filename)
        new_path = os.path.join(IMAGE_DIR, f"{hashed_word}.jpg")
        
        os.rename(old_path, new_path)
        count += 1
        
print(f"Renamed {count} images.")
