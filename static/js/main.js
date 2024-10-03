document.addEventListener('DOMContentLoaded', () => {
    const pairButton = document.getElementById('pairButton');
    const statusDiv = document.getElementById('status');

    pairButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/pair', { method: 'POST' });
            const data = await response.json();
            if (data.success) {
                statusDiv.textContent = 'Armband paired successfully!';
            } else {
                statusDiv.textContent = 'Failed to pair armband. Please try again.';
            }
        } catch (error) {
            console.error('Error:', error);
            statusDiv.textContent = 'An error occurred. Please try again.';
        }
    });
});
