# Technical Debt & Improvements

## Medium Priority
- [ ] **Use Constants for Modes:** Replace magic strings ('vocab', 'math', 'mock_math', etc.) in frontend with a shared constants file or enum.
- [ ] **Fix Naming Inconsistencies:**
    - Standardize backend JSON responses (e.g., `user_answer`, `correct_answer`).
    - Standardize frontend props (camelCase vs snake_case).
- [ ] **Organize Utility Scripts:** Move `download_images.py` and `scraper.py` to a `scripts/` directory.

## Low Priority
- [ ] **E2E Testing:** Implement Playwright/Cypress tests.
- [ ] **Frontend Verification:** Fix timeout issues with `npm test` setup if they persist (currently passing).
- [ ] **Remove Stale Code:** Review usage of `scraper.py` and remove if not needed.
