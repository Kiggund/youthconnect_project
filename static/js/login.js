document.addEventListener('DOMContentLoaded', function() {
    // Password toggle functionality
    document.querySelectorAll('.toggle-password').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const input = this.closest('.input-group').querySelector('input');
            const icon = this.querySelector('i');
            
            // Toggle input type
            const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
            input.setAttribute('type', type);
            
            // Toggle eye icon
            icon.classList.toggle('fa-eye');
            icon.classList.toggle('fa-eye-slash');
            
            // Accessibility - update button label
            const label = type === 'password' ? 'Show password' : 'Hide password';
            this.setAttribute('aria-label', label);
            this.setAttribute('title', label);
        });
    });

    // Add initial accessibility attributes
    document.querySelectorAll('.toggle-password').forEach(button => {
        const input = button.closest('.input-group').querySelector('input');
        const label = input.type === 'password' ? 'Show password' : 'Hide password';
        button.setAttribute('aria-label', label);
        button.setAttribute('role', 'button');
        button.setAttribute('tabindex', '0');
    });
});
