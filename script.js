document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".card").forEach((card, index) => {
        card.style.animationDelay = `${index * 0.2}s`;
    });
});
