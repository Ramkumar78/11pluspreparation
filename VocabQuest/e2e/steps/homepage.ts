import { createBdd } from 'playwright-bdd';
import { expect } from '@playwright/test';

const { Given, Then } = createBdd();

Given('I am on the homepage', async ({ page }) => {
  await page.goto('/');
});

Then('I should see the heading {string}', async ({ page }, text) => {
  await expect(page.getByRole('heading', { name: text })).toBeVisible();
});
