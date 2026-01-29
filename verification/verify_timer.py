from playwright.sync_api import sync_playwright, expect

def verify_timer():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print("Navigating to Game...")
            page.goto("http://localhost:5173/game/math")

            # Wait for game to load (GO! button visible)
            print("Waiting for game load...")
            page.wait_for_selector("button:has-text('GO!')", timeout=10000)

            # Check for Timer Toggle
            timer_btn = page.locator("button:has-text('TIMER OFF')")
            expect(timer_btn).to_be_visible()
            print("Timer button found.")

            # Click Timer
            print("Clicking Timer...")
            timer_btn.click()

            # Verify text changes to Time
            # It starts at 60s
            time_display = page.locator("button", has_text="TIME: 60s")
            expect(time_display).to_be_visible()
            print("Timer started at 60s.")

            # Wait 2 seconds
            page.wait_for_timeout(2000)

            # Check if time decreased (59s or 58s)
            # Regex match for TIME: 5[0-9]s
            timer_active = page.locator("button", has_text="TIME:")
            text = timer_active.inner_text()
            print(f"Timer text after 2s: {text}")

            if "59s" in text or "58s" in text:
                print("Timer is counting down.")
            else:
                print("Timer might not be counting down properly.")

            # Screenshot
            page.screenshot(path="verification/timer_verification.png")
            print("Screenshot saved.")

        except Exception as e:
            print(f"Error: {e}")
            page.screenshot(path="verification/error.png")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_timer()
