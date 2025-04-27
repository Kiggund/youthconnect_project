document.addEventListener('DOMContentLoaded', function () {
    const contactForm = document.getElementById('contactForm');
    const notificationContainer = document.querySelector('.notification-container');

    if (!contactForm) return;

    // Function to display notifications
    function showNotification(type, message) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-icon">
                ${type === 'success' ? '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M21,7L9,19L3.5,13.5L5.91,11.08L9,14.17L18.59,4.59L21,7Z"/></svg>' :
                type === 'error' ? '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M13,16V18H11V16H13M13,6V14H11V6H13Z"/></svg>' :
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M1,21H23L12,2"/></svg>'}
            </div>
            <div class="notification-message">${message}</div>
            <div class="notification-progress"></div>
            <button class="close-btn" aria-label="Close">&times;</button>
        `;

        notificationContainer.appendChild(notification);

        // Handle close button click
        const closeButton = notification.querySelector('.close-btn');
        closeButton.addEventListener('click', () => notification.remove());

        // Auto-remove notification after 5 seconds
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.5s ease forwards';
            notification.addEventListener('animationend', () => notification.remove());
        }, 5000);
    }

    // Handle form submission
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

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.message || `Error: ${response.status}`);
            }

            const data = await response.json();

            // Show success notification
            showNotification('success', data.message);

            // Optionally reset the form after successful submission
            contactForm.reset();

        } catch (error) {
            console.error('Error:', error);
            showNotification('error', error.message || 'An error occurred while sending the message.');
        }
    });
});
