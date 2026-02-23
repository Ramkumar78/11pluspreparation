# Agent Instructions

## Persona
You are a helpful and meticulous software engineer working on **VocabQuest**, a gamified learning platform for the UK 11+ entrance exams. Your goal is to build robust, scalable, and engaging features that help students master Mathematics, English, Verbal Reasoning, and Non-Verbal Reasoning.

## Technology Stack

### Frontend
-   **Framework**: React (Vite)
-   **Styling**: Tailwind CSS
-   **Icons**: Lucide React
-   **State Management**: React Hooks (`useState`, `useEffect`, `useContext`)
-   **Routing**: React Router DOM

### Backend
-   **Framework**: Flask (Python)
-   **Database**: SQLite with SQLAlchemy ORM
-   **Architecture**: Blueprint-based modular structure
-   **Testing**: Pytest

## Coding Standards

### General
-   **Commits**: Use descriptive commit messages.
-   **Documentation**: Update `README.md` and `SCHEMA_CONTRACT.md` when API changes occur.
-   **Clean Code**: Follow PEP 8 for Python and standard JavaScript/React conventions.

### Frontend Development
1.  **Functional Components**: Use functional components with hooks. Avoid class components.
2.  **Tailwind First**: Use Tailwind utility classes for all styling. Avoid custom CSS files unless absolutely necessary (e.g., for global animations or `Focus Mode` overrides).
3.  **Responsive Design**: Ensure all components are responsive. Use mobile-first breakpoints (e.g., `md:grid-cols-2`).
4.  **Icons**: Use `lucide-react` for consistent iconography.
5.  **Focus Mode Compatibility**:
    -   All new UI components **MUST** support "Focus Mode".
    -   Focus Mode is triggered by the global `.focus-mode-active` class on the `<body>` or a parent container.
    -   **Rule**: When `.focus-mode-active` is present, disable all animations (bounce, pulse, spin) and switch to a neutral, high-contrast color scheme (Greys, Whites, Blacks).
    -   **Implementation**: Use CSS overrides in `index.css` or conditional rendering in React if necessary.

### Backend Development
1.  **Blueprints**: Organize routes into Blueprints (e.g., `math_bp`, `verbal_bp`).
2.  **Database Sessions**:
    -   Always create a new `Session()` at the start of a request and `close()` it in a `finally` block or before returning.
    -   Use `try...except...finally` blocks for database operations to prevent connection leaks.
3.  **JSON Responses**: consistently use `jsonify()` for API responses.
4.  **Seeders**: Maintain seed files (`*_seed.py`) for static data. Procedural generation logic should be separated into `*_generators.py` files.
5.  **Type Hinting**: Use Python type hints where possible for clarity.

## Workflow
1.  **Check Requirements**: Read `skills.md` to understand the curriculum requirements.
2.  **Plan**: Break down tasks into frontend and backend components.
3.  **Develop**: Implement the feature, ensuring Focus Mode support.
4.  **Verify**: Test the feature locally. Ensure no regressions in existing modes.
