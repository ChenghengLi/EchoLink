/*
import { generateRandomEmail, generateRandomPassword, generateRandomUsername } from './utils/dataGenerator.js';
import { registerUser, registerArtist } from './utils/user.js';
import { test, expect } from '@playwright/test';


test('Ask and Answer a question', async ({ page }) => {

    // Generate random user data
    const userData = {
        username: generateRandomUsername(),
        email: generateRandomEmail(),
        password: generateRandomPassword(),
    };

    const artistData = {
        username: generateRandomUsername(),
        email: generateRandomEmail(),
        password: generateRandomPassword(),
    };


    // Register an artist
    await registerArtist(artistData.username, artistData.email, artistData.password);

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

    // Click the "My Profile" button
    const profileButton = page.locator('[data-test="profile-laptop"]');
    await expect(profileButton).toBeVisible();
    await profileButton.click();
    await expect(page).toHaveURL(`/users/${userData.username}`);

    // Redirect to dummy 
    await page.goto('/');
    await expect(page).toHaveURL('/');

    // Locate the artist
    const clickableImage = page.locator(`a[href="/users/${artistData.username}"] img.clickable-image`);
    await expect(clickableImage).toBeVisible();

    // Click the artist
    await clickableImage.click();
    await expect(page).toHaveURL(`/users/${artistData.username}`);

    // Locate the button to ask a question
    const askQuestionButton = page.locator('[data-test="button-ask"]');
    await expect(askQuestionButton).toBeVisible();
    await askQuestionButton.click();

    // Locate the input field
    const textarea = page.locator('textarea[id="swal-input"]');
    await expect(textarea).toBeVisible();
    await textarea.fill('Hello, how are you?');

    // Locate the Send button
    const sendButton = page.locator('button:has-text("Send")');
    await expect(sendButton).toBeVisible();
    await sendButton.click();

    // Locate the success toast
    const successToastQuestion = page.locator('text="Your question has been sent successfully!"');
    await expect(successToastQuestion).toBeVisible();

    // Check the URL is correct
    await expect(page).toHaveURL(`/users/${artistData.username}`);

    // Locate the button to ask a question
    await expect(askQuestionButton).toBeVisible();
    await askQuestionButton.click();

    // Locate the input field
    await expect(textarea).toBeVisible();
    await textarea.fill('Nice to meet you!');

    // Locate the Send button
    await expect(sendButton).toBeVisible();
    await sendButton.click();

    // Locate the error toast
    const okButton = page.locator('button:has-text("OK")');
    await expect(okButton).toBeVisible();
    await okButton.click();

    // Check the URL is correct
    await expect(page).toHaveURL(`/users/${artistData.username}`);

    // Log out
    const logoutButton = page.locator('[data-test="logout-laptop"]');
    await expect(logoutButton).toBeVisible();
    await logoutButton.click();

    // Log in as the artist
    await page.goto('/logIn');
    await expect(page).toHaveURL('/logIn');

    // Fill the login form with the artist data
    await emailInput.fill(artistData.email);
    await emailInput.press('Enter');

    await passwordInput.fill(artistData.password);
    await passwordInput.press('Enter');

    // Check the success toast
    await expect(successToast).toBeVisible();

    // Locate the Dashboard button
    const dashboardButton = page.getByRole('button', { name: 'Dashboard' });
    await expect(dashboardButton).toBeVisible();
    await dashboardButton.click();

    // Check the URL is correct
    await expect(page).toHaveURL('/dashboard');

    // Locate the question
    const questionDiv = page.locator('div.question.relative.group');
    await expect(questionDiv).toBeVisible();
    await questionDiv.hover();

    // Locate the answer button
    const answerButton = page.locator('button:has-text("Answer")').nth(1);
    await expect(answerButton).toBeVisible();
    await answerButton.click();

    // Locate the fields
    const answerInput = page.locator('textarea[id="swal-input"]');
    await expect(answerInput).toBeVisible();
    await answerInput.fill('I am fine, thank you!');

    // Locate the Send button
    const sendResponseButton = page.locator('button:has-text("Send Response")');
    await expect(sendResponseButton).toBeVisible();
    await sendResponseButton.click();

    // Locate the success toast
    const successToastAnswer = page.locator('text="Your response has been sent successfully!"');
    await expect(successToastAnswer).toBeVisible();
});
*/