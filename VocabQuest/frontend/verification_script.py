
from playwright.sync_api import sync_playwright, expect

def test_comprehension_image(page):
    # 1. Navigate to home
    page.goto("http://localhost:5173")

    # 2. Click on "PLAY COMP"
    page.get_by_text("PLAY COMP").click()

    # 3. Wait for passage to load
    # It should show a passage and hopefully an image.
    page.wait_for_selector("img", timeout=10000) # Wait for any image

    # 4. Expect an image with comprehension in src or similar, or just any image in the passage area.
    # The Game.jsx has: <img src={gameState.image_url} ... />

    expect(page.locator("img").first).to_be_visible()

    # 5. Take screenshot
    page.screenshot(path="/home/jules/verification/comprehension_ui.png")

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_comprehension_image(page)
        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="/home/jules/verification/error.png")
        finally:
            browser.close()
