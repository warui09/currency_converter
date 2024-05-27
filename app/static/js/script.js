document.addEventListener('DOMContentLoaded', (event) => {
    const form = document.getElementById('currency-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

	const form = document.getElementById('currency-form');
        const formData = new FormData(form);
        const data = {
            amount: formData.get('amount'),
            source_currency: formData.get('source_currency'),
            target_currency: formData.get('target_currency')
        };

        try {
            const response = await fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const result = await response.json();
            document.getElementById('result').innerHTML = `Converted Amount: ${result.converted_amount}`;
        } catch (error) {
            document.getElementById('result').innerHTML = `Error: ${error.message}`;
        }
    });
});
