import { defineConfig, devices } from '@playwright/test';
import { defineBddConfig } from 'playwright-bdd';

const bddTestDir = defineBddConfig({
  features: 'features/*.feature',
  steps: 'steps/*.ts',
});

export default defineConfig({
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'bdd',
      testDir: bddTestDir,
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'e2e',
      testDir: '.',
      testMatch: ['**/*.spec.ts'],
      testIgnore: ['**/.features-gen/**'],
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
