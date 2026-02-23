# UI Guidelines

## Visual Philosophy

VocabQuest balances two distinct visual modes:
1.  **Playful (Default)**: Bright, engaging, gamified. Uses gradients, animations (bounce, pulse), and "juice" (feedback effects).
2.  **Focus Mode**: Strict, distraction-free. Grey/White/Black palette only. No animations. High contrast.

## Color Palette

### Standard (Playful)
-   **Primary**: Indigo (`indigo-600` to `indigo-900`)
-   **Accents**: Fuchsia (`fuchsia-500`), Violet (`violet-500`), Emerald (`emerald-500` for success), Rose (`rose-500` for error).
-   **Backgrounds**: Gradients (`bg-gradient-to-br from-indigo-500 to-purple-600`).

### Focus Mode
-   **Background**: `gray-100` (#f3f4f6)
-   **Surface**: `white` (#ffffff)
-   **Text**: `gray-800` (#1f2937)
-   **Borders**: `gray-200` (#e5e7eb)

## Focus Mode Implementation

Focus Mode is controlled by the `FocusHeader` component in `App.jsx`, which toggles the `.focus-mode-active` class on the root container.

### Rules for New Components
1.  **No Hardcoded Colors**: Avoid `style={{ color: 'red' }}`. Use Tailwind classes.
2.  **CSS Overrides**: The global `index.css` contains overrides for `.focus-mode-active`.
    -   It forces all gradients to `gray-100`.
    -   It forces `text-white` to `text-gray-800` (except on buttons).
    -   It disables animations.
3.  **Conditional Rendering**: If a component is purely decorative (e.g., a bouncing mascot), hide it in Focus Mode:
    ```jsx
    <div className="focus-mode-active:hidden">
      <BouncingMascot />
    </div>
    ```

## Component Library (Standard)

### Buttons
-   **Action**: `bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl shadow-lg transition-transform hover:scale-105 active:scale-95`
-   **Secondary**: `bg-white text-indigo-600 border-2 border-indigo-100 hover:bg-indigo-50`

### Cards
-   **Glassmorphism (Default)**: `bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl shadow-xl`
-   **Standard**: `bg-white rounded-2xl shadow-md border border-gray-100`

### Typography
-   **Headings**: `font-black text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600`
-   **Body**: `text-gray-600 font-medium`

## Icons
Use `lucide-react` for all icons.
-   Common: `BookOpen`, `Zap` (Streak), `Trophy` (Leaderboard), `Lightbulb` (Hint).
