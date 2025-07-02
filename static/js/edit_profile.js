document.addEventListener('DOMContentLoaded', function() {
    // File upload preview and filename display
    const fileInput = document.querySelector('#id_profile_pic');
    const fileInfo = document.querySelector('.file-info');
    const currentPic = document.querySelector('.current-pic');
    
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            if (this.files && this.files[0]) {
                // Display filename
                fileInfo.textContent = this.files[0].name;
                
                // Preview image
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Remove default icon if exists
                    const defaultIcon = currentPic.querySelector('.default-pic');
                    if (defaultIcon) {
                        defaultIcon.remove();
                    }
                    
                    // Check if img already exists
                    let img = currentPic.querySelector('img');
                    if (!img) {
                        img = document.createElement('img');
                        img.classList.add('profile-image');
                        currentPic.appendChild(img);
                    }
                    
                    img.src = e.target.result;
                }
                reader.readAsDataURL(this.files[0]);
            }
        });
    }
    
    // Show current filename if editing existing profile
    if (fileInput && fileInput.files.length > 0) {
        fileInfo.textContent = fileInput.files[0].name;
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Handle form submission
    const form = document.querySelector('.profile-form');
    if (form) {
        form.addEventListener('submit', function() {
            // Get the 'next' parameter from URL
            const urlParams = new URLSearchParams(window.location.search);
            const nextUrl = urlParams.get('next');
            
            // If we have a next URL, store it in localStorage
            if (nextUrl) {
                localStorage.setItem('profile_edit_redirect', nextUrl);
            }
        });
    }
    
    // Check for successful save redirect
    if (performance.navigation.type === performance.navigation.TYPE_RELOAD) {
        const redirectUrl = localStorage.getItem('profile_edit_redirect');
        if (redirectUrl) {
            localStorage.removeItem('profile_edit_redirect');
            window.location.href = redirectUrl;
        }
    }
});
