const btn1 = document.getElementById('team-btn-2');
const btn2 = document.getElementById('team-btn-3');
const element = document.querySelectorAll('.team-main-card-wrap-btn-1.team-active');
const rotCont = document.querySelector('.team-rotate-wrap-2');
const rotCont1 = document.querySelector('.team-rotate-wrap-1');
const contentMain = document.querySelector('.team-main-card-col-10');
const inset = document.querySelector('.team-main-cards .team-main-card-2-wrap:nth-child(1)');

function contentFunc1() {
    element[1].classList.toggle('hidden');
    rotCont.classList.toggle('team-rotate');
    btn2.classList.toggle('team-back')
    contentMain.classList.toggle('clock');
    inset.classList.toggle('inset')
}

/* function contentFunc() {
    element[0].classList.toggle('hidden');
    rotCont1.classList.toggle('team-rotate');
    btn1.classList.toggle('team-back');
} */


/* btn1.addEventListener('click', contentFunc); */
btn2.addEventListener('click', contentFunc1);


const partnerBtn = document.querySelector('.partner-main-wrap-col-2-btn');
const partnerContent1 = document.querySelector('.partner-main-wrap-col-2-content');

function partnerContent() {
    partnerBtn.classList.toggle('partner-btn-active');
    partnerContent1.classList.toggle('partner-content-main-col')
}

partnerBtn.addEventListener('click', partnerContent);

/*  Partner card */

const partnerBtn1 = document.querySelector('.partner-btn');
const partnerCard = document.querySelector('.partner-card-1:last-child');

function partnerCard1() {
    partnerCard.classList.toggle('partner-card-active')
}

partnerBtn1.addEventListener('click', partnerCard1)

/*  Partner search */

const teamBtn1 = document.querySelector('.team-btn-1');
const teamBtn2 = document.querySelector('.team-btn-2');
const teamCont1 = document.querySelector('.team-right-main-wrap');
const teamCont2 = document.querySelector('.partner-right-main-wrap-2')

function teamContent1() {
    teamCont1.classList.add('team-right-main-active');
    teamCont2.classList.add('partner-right-main-active');
    teamBtn1.classList.add('team-main-btn-active');
    teamBtn2.classList.add('team-main-btn-active-2')
}

function teamContent2() {
    teamCont1.classList.remove('team-right-main-active');
    teamCont2.classList.remove('partner-right-main-active');
    teamBtn1.classList.remove('team-main-btn-active');
    teamBtn2.classList.remove('team-main-btn-active-2')
}

teamBtn1.addEventListener('click', teamContent1);
teamBtn2.addEventListener('click', teamContent2);

/*  Search main */

const mainBtn = document.querySelector('.partner-main-wrap-col-btn');
const mainPartner = document.querySelector('.partner-fixed-content');
const mainPartnerInner = document.querySelector('.partner-fixed-wrap');

function mainContent(event) {
    mainPartner.classList.toggle('partner-fixed-active');
}

mainBtn.addEventListener('click', mainContent);

mainPartnerInner.addEventListener('click', (event) => {
    event.stopPropagation();
});

mainPartner.addEventListener('click', (event) => {
    if (!mainPartnerInner.contains(event.target)) {
        mainPartner.classList.remove('partner-fixed-active');
    }
});
