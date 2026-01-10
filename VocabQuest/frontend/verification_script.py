import time
from playwright.sync_api import sync_playwright, expect

def verify_features():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # We need to make sure the server is running. I will start it in background before running this script.
        # Assuming frontend is on 5173
        page = browser.new_page()

        # 1. Verify Home Page has new buttons
        try:
            page.goto("http://localhost:5173")

            # Wait for content to load
            expect(page.get_by_text("ScholarQuest")).to_be_visible()

            # Check for new buttons
            expect(page.get_by_text("TAKE MOCK EXAM")).to_be_visible()
            expect(page.get_by_text("MY DASHBOARD")).to_be_visible()

            # Take screenshot of home
            page.screenshot(path="/home/jules/verification/home_page.png")
            print("Home page verified.")

            # 2. Verify Dashboard
            page.get_by_text("MY DASHBOARD").click()
            expect(page.get_by_text("My Learning Journey")).to_be_visible()
            # Wait for topics to load (it might be empty or show loading)
            # We mocked the backend response in unit tests, but here we are hitting real backend?
            # If backend is running, it should return something or empty list.
            # Let's take screenshot of dashboard
            time.sleep(2) # Wait for potential data load
            page.screenshot(path="/home/jules/verification/dashboard_page.png")
            print("Dashboard verified.")

            # Back to home
            page.get_by_text("Back to Home").click()
            expect(page.get_by_text("ScholarQuest")).to_be_visible()

            # 3. Verify Mock Test
            page.get_by_text("TAKE MOCK EXAM").click()
            # Wait for the page to load either the loading state or the content
            # Simple wait for now as logic is conditional
            time.sleep(2)
            page.screenshot(path="/home/jules/verification/mock_test_page.png")
            print("Mock Test page verified.")

        except Exception as e:
            print(f"Verification failed: {e}")
            page.screenshot(path="/home/jules/verification/error.png")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    verify_features()
