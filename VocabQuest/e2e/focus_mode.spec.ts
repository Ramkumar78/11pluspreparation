import { test, expect } from '@playwright/test';

test('Focus Mode toggles correctly and updates styles', async ({ page }) => {
  // 1. Navigate to homepage
  await page.goto('/');

  // 2. Trigger Focus Mode
  // Click the label text "Focus Mode" because the input is hidden (sr-only)
  // and covered by the custom toggle styling.
  await page.getByText('Focus Mode').click();

  // 3. Verify .focus-mode-active class on root container
  const appContainer = page.locator('.focus-mode-active');
  await expect(appContainer).toBeVisible();

  // 4. Verify computed styles
  // Background color: gray-100 -> rgb(243, 244, 246)
  await expect(appContainer).toHaveCSS('background-color', 'rgb(243, 244, 246)');
  // Text color: gray-800 -> rgb(31, 41, 55)
  await expect(appContainer).toHaveCSS('color', 'rgb(31, 41, 55)');

  // 5. Verify animation-free
  // The bouncing lion should be hidden.
  const bouncingLion = page.locator('.animate-bounce');
  await expect(bouncingLion).toBeHidden();
});
