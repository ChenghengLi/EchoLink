import axios from 'axios';
import { API_CONFIG } from '../config';

describe('Backend Connection Test', () => {
  it('should get "Hello World!" response from the backend', async () => {
    // Arrange: Define the expected response
    const expectedResponse = 'Hello World!';

    // Act: Make the POST request
    const response = await axios.post(`${API_CONFIG.BASE_URL}/test/test`);

    // Assert: Check if the response data matches the expected response
    expect(response.data).toBe(expectedResponse);
  });
});