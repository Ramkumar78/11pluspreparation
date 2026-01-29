# Technical Debt & Improvements

## Medium Priority
- [ ] **Refactor Backend Architecture:** Split `VocabQuest/backend/app.py` (currently ~400 lines) into Flask Blueprints (e.g., `auth`, `math`, `vocab`, `comprehension`, `mock`) to improve maintainability.
- [ ] **Implement React Router:** Replace the current state-based routing (`view` state in `App.jsx`) with `react-router-dom` for better navigation and URL handling.
- [ ] **Organize Utility Scripts:** Move backend utility scripts (`download_images.py`, `scraper.py`, `download_comprehension_images.py`) to a dedicated `backend/scripts/` directory and update imports/paths.
- [ ] **Use Constants for Modes:** Replace magic strings ('vocab', 'math', 'mock_math', etc.) in `App.jsx` and `Home.jsx` with a shared constants file or enum.

## Low Priority
- [ ] **E2E Testing:** Implement a proper E2E testing suite (using Playwright or Cypress) integrated into the CI pipeline, replacing ad-hoc scripts.
- [ ] **Frontend Verification:** Fix the timeout issues with `npm test` setup if persistent.
