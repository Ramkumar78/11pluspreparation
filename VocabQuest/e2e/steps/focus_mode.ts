import { createBdd } from 'playwright-bdd';
import { expect } from '@playwright/test';

const { When, Then } = createBdd();

// Given step is reused from homepage.ts

Then('I should see the {string} toggle', async ({ page }, text) => {
  await expect(page.getByText(text)).toBeVisible();
});

Then('I should see the session timer', async ({ page }) => {
  await expect(page.getByText('⏱')).toBeVisible();
  const timerText = await page.getByText('⏱').locator('..').textContent();
  expect(timerText).toMatch(/⏱\d{2}:\d{2}:\d{2}/);
});

When('I toggle Focus Mode on', async ({ page }) => {
  await page.locator('label').filter({ hasText: 'Focus Mode' }).click();
});

Then('the background should be neutral', async ({ page }) => {
  const appWrapper = page.locator('.focus-mode-active');
  await expect(appWrapper).toBeVisible();
  const bgColor = await appWrapper.evaluate((el) => {
    return window.getComputedStyle(el).backgroundColor;
  });
  expect(bgColor).toBe('rgb(243, 244, 246)');
});

Then('the bouncing lion should be hidden', async ({ page }) => {
  const lion = page.getByText('🦁');
  await expect(lion).toBeHidden();
});

Then('the timer should be counting', async ({ page }) => {
  const timerLocator = page.getByText('⏱').locator('..');
  const text1 = await timerLocator.textContent();
  await page.waitForTimeout(2000);
  const text2 = await timerLocator.textContent();
  expect(text1).not.toEqual(text2);
});
