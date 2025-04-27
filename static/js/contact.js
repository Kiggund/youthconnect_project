document.addEventListener('DOMContentLoaded', function () {
    const contactForm = document.getElementById('contactForm');
    if (!contactForm) return;

    contactForm.addEventListener('submit', async function (e) {
        e.preventDefault(); // Prevent the default form submission

        try {
            const formData = new FormData(contactForm);
            const csrfToken = document.cookie
                .split('; ')
                .find(row => row.startsWith('csrftoken='))
                ?.split('=')[1];

            const response = await fetch(contactForm.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest', // Critical AJAX header
                    'X-CSRFToken': csrfToken  // CSRF token from cookie
                },
                credentials: 'include'  // Include credentials for CSRF protection
            });

            const data = await response.json();
            console.log(data); // Log response for debugging
            alert(data.message); // Provide feedback to the user
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while sending the message.');
        }
    });
});
