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


function copyReferralLink(referralValue) {
    var fullLink = "https://s1.sublar.kz/register/?ref=" + referralValue;
    if (navigator.clipboard && window.isSecureContext) {
        // Используем асинхронное API
        navigator.clipboard.writeText(fullLink)
            .then(function() {
                alert("Реферальная ссылка скопирована: " + fullLink);
            })
            .catch(function(err) {
                console.error("Ошибка копирования:", err);
            });
    } else {
        // Фолбэк для небезопасного контекста или старых браузеров
        var tempInput = document.createElement("input");
        tempInput.style.position = "absolute";
        tempInput.style.left = "-1000px";
        tempInput.value = fullLink;
        document.body.appendChild(tempInput);
        tempInput.select();
        try {
            document.execCommand("copy");
            alert("Реферальная ссылка скопирована: " + fullLink);
        } catch (err) {
            console.error("Ошибка копирования:", err);
        }
        document.body.removeChild(tempInput);
    }
}



