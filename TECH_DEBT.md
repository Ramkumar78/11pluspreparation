# Technical Debt & Improvements

## Medium Priority
- [ ] **Fix Naming Inconsistencies:**
    - Standardize backend JSON responses (e.g., `user_answer`, `correct_answer`).
    - Standardize frontend props (camelCase vs snake_case).

## Low Priority
- [ ] **E2E Testing:** Implement Playwright/Cypress tests.
- [ ] **Frontend Verification:** Fix timeout issues with `npm test` setup if they persist (currently passing).
- [ ] **Script Testing:** Add unit tests for utility scripts in `backend/scripts/`.
- [ ] **Port Configuration:** Standardize port usage between local dev (5000 vs 5001) and Docker to avoid confusion.
