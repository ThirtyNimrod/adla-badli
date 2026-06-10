import { test, expect } from '@playwright/test';

test.describe('Adla-Badli Homepage', () => {
  test('should load successfully and show app title', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle(/Adla-Badli/);
    await expect(page.locator('#app-title')).toHaveText('Adla-Badli');
  });

  test('should have file upload dropzone', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('#file-dropzone')).toBeVisible();
  });
});
