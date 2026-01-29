# Technical Debt & Improvements

## High Priority
- [ ] **Missing Authentication:** Implement multi-user support and authentication (UserStats is currently global).

## Medium Priority
- [ ] **Design Pattern:** Decouple database initialization (`init_db`) from application startup logic.

## Low Priority
- [ ] **E2E Testing:** Implement Playwright/Cypress tests.
- [ ] **Port Configuration:** Standardize port usage between local dev (5000 vs 5001) and Docker to avoid confusion.
- [ ] **Remove Hardcoded URLs:** Replace `http://localhost:5001` with environment variable or relative path proxy.
- [ ] **Logging:** Replace print statements with a proper logging configuration.
