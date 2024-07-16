// home.js
const card = document.querySelector('.card3d');
const flipButton = document.getElementById('flip-button');

card.addEventListener('mousemove', (e) => {
    const cardRect = card.getBoundingClientRect();
    const cardCenterX = cardRect.left + cardRect.width / 2;
    const cardCenterY = cardRect.top + cardRect.height / 2;

    // Calculate mouse position relative to card center
    const mouseX = e.clientX;
    const mouseY = e.clientY;
    const deltaX = mouseX - cardCenterX;
    const deltaY = mouseY - cardCenterY;

    // Calculate rotation angles
    const rotateY = deltaX / 10; // Adjust sensitivity as needed
    const rotateX = -deltaY / 10; // Adjust sensitivity as needed

    // Apply transform to the card
    card.style.transform = `translateY(-20px) rotateX(10deg) rotateY(5deg) rotateY(${rotateY}deg) rotateX(${rotateX}deg)`;
});

card.addEventListener('mouseleave', () => {
    // Reset transform on mouse leave
    card.style.transform = 'translateY(-20px) rotateX(10deg) rotateY(5deg)';
});

flipButton.addEventListener('click', () => {
    flipButton.classList.add('flip');
    setTimeout(() => {
        window.location.href = 'http://127.0.0.1:5000/login';
    }, 1000); // Adjust delay as per animation duration
});
