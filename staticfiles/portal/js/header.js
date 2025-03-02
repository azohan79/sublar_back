document.addEventListener('DOMContentLoaded', function () {
    const btn = document.getElementById('banner');
    const btn2 = document.getElementById('banner1');

    const content = document.querySelector('.header-mobile-content');
    const body = document.body;

    function mybtn() {
        if (content.style.display === 'none' || getComputedStyle(content).display === 'none') {
            content.style.display = 'block';
            body.classList.toggle('ac');
        } else {
            content.style.display = 'none';
            body.classList.toggle('ac');
        }
    }

    btn.addEventListener('click', mybtn);
    btn2.addEventListener('click', mybtn);
});
