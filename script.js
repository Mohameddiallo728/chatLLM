document.addEventListener("DOMContentLoaded", function() {
    const messages = document.querySelectorAll(".message");
    messages.forEach((message, index) => {
        setTimeout(() => {
            message.classList.add("fade-in");
        }, index * 100);
    });
});