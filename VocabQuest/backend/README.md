# Backend

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Image Download

The application uses local images for vocabulary words. To download these images:

1. Run the download script:
   ```bash
   python scripts/download_images.py
   ```
   This script fetches images from `pollinations.ai` for words listed in `seed_list.py` and saves them to `../frontend/public/images`.
   Note: The download might take some time due to rate limiting.

## Running the App

1. Start the Flask server:
   ```bash
   python app.py
   ```

## Testing

1. Run tests:
   ```bash
   pytest
   ```
