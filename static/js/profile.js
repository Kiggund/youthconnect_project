document.addEventListener("DOMContentLoaded", function() {
    const profilePicInput = document.querySelector("input[name='profile_picture']");
    const profilePicPreview = document.querySelector("#profile-preview");
    const notificationContainer = document.querySelector(".notification-container");
    const form = document.querySelector("#profile-form");
    const toggleBtn = document.getElementById("theme-toggle");
    const body = document.body;

    // Load saved theme preference
    if (localStorage.getItem("theme") === "dark") {
        body.classList.add("dark");
        toggleThemeIcon();
    }

    // Theme toggle listener
    toggleBtn?.addEventListener("click", function () {
        body.classList.toggle("dark");
        const theme = body.classList.contains("dark") ? "dark" : "light";
        localStorage.setItem("theme", theme);
        toggleThemeIcon();
    });

    function toggleThemeIcon() {
        const icon = toggleBtn.querySelector("i");
        if (icon) {
            icon.classList.toggle("fa-moon");
            icon.classList.toggle("fa-sun");
        }
    }

    // Preview profile picture before uploading
    profilePicInput?.addEventListener("change", function(event) {
        const file = event.target.files[0];
        if (file && file.type.startsWith("image/")) {
            const reader = new FileReader();
            reader.onload = function(e) {
                profilePicPreview.src = e.target.result;
            };
            reader.readAsDataURL(file);
        } else {
            showNotification("Invalid file type. Please upload an image.", "error");
        }
    });

    // Auto-save profile updates using AJAX
    form?.addEventListener("input", function() {
        const formData = new FormData(form);
        fetch("/accounts/edit/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": document.querySelector("input[name='csrfmiddlewaretoken']").value
            }
        })
        .then(response => response.json())
        .then(() => showNotification("Profile updated successfully!", "success"))
        .catch(() => showNotification("Failed to save changes.", "error"));
    });

    function showNotification(message, type) {
        const notification = document.createElement("div");
        notification.className = `notification ${type}`;
        notification.innerText = message;
        notificationContainer?.appendChild(notification);

        setTimeout(() => {
            notification.remove();
        }, 3000);
    }
});
