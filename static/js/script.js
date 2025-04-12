document.addEventListener("DOMContentLoaded", function () {
    const words = ["Welcome", "to", "Youth Connect"]; // Words to animate
    const container = document.getElementById("animated-text"); // Target container

    let index = 0; // Current word index

    function displayWord() {
        if (index < words.length) {
            const span = document.createElement("span");
            span.textContent = words[index]; // Add the current word
            span.className = "animated-word"; // Add a class for styling

            // Apply random color for each word
            span.style.color = `hsl(${Math.random() * 360}, 70%, 50%)`;
            span.style.opacity = 0; // Initially hidden
            span.style.transition = "opacity 1s ease"; // Smooth fade-in

            container.appendChild(span); // Add span to the container

            // Fade in the word
            setTimeout(() => {
                span.style.opacity = 1;
            }, 100);

            index++; // Move to the next word
            setTimeout(displayWord, 1500); // Display next word after 1.5 seconds
        } else {
            // Fade out the entire container after the last word
            setTimeout(() => {
                container.style.opacity = 1; // Ensure visibility before fading
                container.style.transition = "opacity 2s ease"; // Fade-out transition
                container.style.opacity = 0; // Fade out

                setTimeout(() => {
                    container.innerHTML = ""; // Clear all words
                    container.style.opacity = 1; // Reset opacity for next loop
                    index = 0; // Reset word index
                    displayWord(); // Restart animation
                }, 2000); // Delay for fade-out duration
            }, 1500); // Wait after the last word
        }
    }

    displayWord(); // Start the animation
});
