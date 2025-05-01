document.addEventListener('DOMContentLoaded', function () {
    const notificationContainer = document.querySelector('.notification-container');

    function showNotification(type, message) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-icon">
                ${
                    type === 'error'
                        ? '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path fill="currentColor" d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M13,16V18H11V16H13M13,6V14H11V6H13Z"/></svg>'
                        : ''
                }
            </div>
            <div class="notification-message">${message}</div>
            <div class="notification-progress"></div>
            <button class="close-btn" aria-label="Close">&times;</button>
        `;

        notificationContainer.appendChild(notification);

        const closeButton = notification.querySelector('.close-btn');
        closeButton.addEventListener('click', () => notification.remove());

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.5s ease forwards';
            notification.addEventListener('animationend', () => notification.remove());
        }, 5000);
    }

    // Simulate an error notification (example for testing)
    showNotification('error', 'Too many attempts. Please wait 15 minutes.');
});
