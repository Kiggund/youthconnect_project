document.addEventListener("DOMContentLoaded", function () {
    function togglePassword(fieldId, button) {
        var passwordField = document.getElementById(fieldId);
        var icon = button.querySelector("i");

        if (passwordField.type === "password") {
            passwordField.type = "text";
            icon.classList.remove("fa-eye");
            icon.classList.add("fa-eye-slash");
        } else {
            passwordField.type = "password";
            icon.classList.remove("fa-eye-slash");
            icon.classList.add("fa-eye");
        }
    }

    // Apply event listeners to all password toggles
    document.querySelectorAll(".toggle-password").forEach(button => {
        button.addEventListener("click", function () {
            togglePassword(this.previousElementSibling.id, this);
        });
    });
});
