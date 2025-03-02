const buttons = document.querySelectorAll('.new-button-bottom');
const slider = document.querySelector('.new-slider');

function goToSlide(slideIndex) {
    const slideWidth = slider.offsetWidth;
    slider.scrollLeft = slideIndex * slideWidth;

    buttons.forEach((button, index) => {
        if (index === slideIndex) {
            button.classList.add('active');
        } else {
            button.classList.remove('active');
        }
    });
}

buttons.forEach((button) => {
    button.addEventListener('click', () => {
        const slideIndex = parseInt(button.getAttribute('data-slide'));
        goToSlide(slideIndex);
    });
});
