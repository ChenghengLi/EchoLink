import { generateRandomEmail, generateRandomPassword, generateRandomUsername } from './utils/dataGenerator.js';
import { registerUser } from './utils/user.js';
import { test, expect } from '@playwright/test';


test('Log In Successful', async ({ page }) => {

    // Generate random user data
    const userData = {
        username: generateRandomUsername(),
        email: generateRandomEmail(),
        password: generateRandomPassword(),
    };


    // Register a new user
    await registerUser(userData.username, userData.email, userData.password);

    await page.goto('/logIn');
    await expect(page).toHaveURL('/logIn');

    const emailInput = page.locator('[data-test="field-email"]');
    await emailInput.fill(userData.email);
    await emailInput.press('Enter');

    const passwordInput = page.locator('[data-test="field-password"]');
    await passwordInput.fill(userData.password);
    await passwordInput.press('Enter');

    const successToast = page.locator('text="Log in successful!"');
    await expect(successToast).toBeVisible();

});


test('Unsuccessful login with unassociated email', async ({ page }) => {


    // Navigate to the login page
    await page.goto('/logIn');
    await expect(page).toHaveURL('/logIn');

    // Attempt to log in with an email that is not associated with any account
    const emailInput = page.locator('[data-test="field-email"]');
    await emailInput.fill(generateRandomEmail());

    const passwordInput = page.locator('[data-test="field-password"]');
    await passwordInput.fill('validpassword');
    await passwordInput.press('Enter');

    // Verify that a SweetAlert2 error popup appears with the appropriate message
    const errorPopup = page.locator('.swal2-popup .swal2-title');
    await expect(errorPopup).toHaveText('Log in failed');

    // Verify the specific error message
    const errorMessage = page.locator('.swal2-popup .swal2-html-container');
    await expect(errorMessage).toHaveText('Reason: The email is not associated to any account.');

});

test('Unsuccessful login with incorrect password', async ({ page }) => {

    // Generate random user data
    const userData = {
        username: generateRandomUsername(),
        email: generateRandomEmail(),
        password: generateRandomPassword(),
    };


    // Register a new user
    await registerUser(userData.username, userData.email, userData.password);


    // Navigate to the login page
    await page.goto('/logIn');
    await expect(page).toHaveURL('/logIn');

    // Enter a valid email that is associated with an account
    const emailInput = page.locator('[data-test="field-email"]');
    await emailInput.fill(userData.email);

    // Enter an incorrect password
    const passwordInput = page.locator('[data-test="field-password"]');
    await passwordInput.fill('wrongpassword');
    await passwordInput.press('Enter');

    // Verify that a SweetAlert2 error popup appears with the appropriate message
    const errorPopup = page.locator('.swal2-popup .swal2-title');
    await expect(errorPopup).toHaveText('Log in failed');

    // Verify the specific error message
    const errorMessage = page.locator('.swal2-popup .swal2-html-container');
    await expect(errorMessage).toHaveText('Reason: Incorrect password.');

});



