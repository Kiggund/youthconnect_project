document.getElementById("contactForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevents page reload

    let formData = new FormData(this);

    fetch('/send-message/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showPopup(data.message); // Call function to show pop-up
        } else {
            alert(data.message); // Shows error message if submission fails
        }
    })
    .catch(error => console.error("Error:", error));
});

// Function to show pop-up notification
function showPopup(message) {
    let popup = document.getElementById("popupNotification");
    popup.innerText = message;
    popup.classList.add("active");

    setTimeout(() => {
        popup.classList.remove("active");
    }, 3000); // Disappears after 3 seconds
}
