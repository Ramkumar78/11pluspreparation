# Technical Debt & Improvements

## High Priority
- [ ] **Missing Authentication:** Implement multi-user support and authentication (UserStats is currently global).

## Medium Priority
- [ ] **Database Side Effects:** `database.py` executes `create_all` and `migrate_db` on import. Move to a CLI command or factory pattern.
- [ ] **Logging:** Replace `print` statements with a proper logging configuration.

## Low Priority
- [ ] **E2E Testing:** Implement Playwright/Cypress tests.
- [ ] **Port Configuration:** Standardize port usage between local dev (5000 vs 5001) and Docker.
