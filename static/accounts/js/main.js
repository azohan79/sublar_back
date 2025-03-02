$(document).ready(function () {
    const ctx = document.getElementById('myChart');
    if (ctx) {
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [6, 1],
                    backgroundColor: [
                        '#FF015C',
                        '#393F49',
                    ],
                    hoverOffset: 0,
                    borderColor: 'transparent',
                    borderWidth: 0,
                }]
            },

        });
    }
    if($('.cart-btn').length || $('.cart-checkbox').length) {
        $('.cart-checkbox').on('click', function () {
            if($('.cart-checkbox:not(:checked)').length != 0) {
                $('.cart-btn').addClass('disabled');
            } else {
                $('.cart-btn').removeClass('disabled');
            }
        });

    }
    $('body').on('click', function () {
        $('*').removeClass('select-active');
        $('.header__notifications').removeClass('active');
    });
    $('.team__body-filters-mob-head').on('click', function () {
        $(this).siblings().slideToggle();
    });
    $('.link-bottom .team-tree-card__link').on('click', function () {
        $(this).parent().parent().toggleClass('active');
        $(this).toggleClass('active');
    });
    $('.link-top .team-tree-card__link').on('click', function () {
        $(this).parent().parent().toggleClass('active');
        $(this).toggleClass('active');
    });
    $(document).ready(function() {
        $(".all").on("change", function() {
            var groupId = $(this).data('id');
            $('.one[data-id="' + groupId + '"]').prop("checked", this.checked);
        });

        $(".one").on("change", function() {
            var groupId = $(this).data('id');
            var allChecked = $('.one[data-id="' + groupId + '"]:not(:checked)').length == 0;
            $('.all[data-id="' + groupId + '"]').prop("checked", allChecked);
        });
    });
    $('.select-head').on('click', function(e) {
        $('*').not($(this).parent()).removeClass('select-active');
        $(this).parent().toggleClass('select-active');
        e.stopPropagation();
    });
    $(".select-option").on('click', function() {
        $(this).siblings('.select-option').removeClass('option-active');
        $(this).addClass('option-active');
        let optionValue = $(this).children('label').text();
        $(this).parent().parent('.select-body').siblings('.select-head').children('.select-side').children(".select-value").text(optionValue);
        $(this).parent().parent().parent().removeClass('select-active');
        if ($(this).children('.catalog__filter-block-option-text').children('.catalog__filter-block-option-text-img').length) {
            var $img = $(this).children('.catalog__filter-block-option-text').children('.catalog__filter-block-option-text-img').clone();
            $(this).parent().parent('.select-body').siblings('.select-head').children('.select-side').children(".catalog__filter-block-head-logo").html($img);
        } else {
            $(this).parent().parent('.select-body').siblings('.select-head').children('.select-side').children(".catalog__filter-block-head-logo").html('');
        }
    });
    $('.tool-link').on('click', function(e) {
        let tools = $(".tool-block-" + $(this).attr('data-tool-link'));
        $(this).siblings($('.tool-link')).removeClass('active');
        $(this).addClass('active');
        tools.siblings($('.tool-block')).removeClass('active');
        tools.addClass('active');
        e.preventDefault();
    });
    $(".form-block__input-button").mousedown(function(e){
        $(this).prev().attr('type','text');
        $(this).addClass('active');
        e.stopPropagation();
    }).mouseup(function(e){
        $(this).removeClass('active');
        $(this).prev().attr('type','password');
        e.stopPropagation();
    });
    $('.header__burger').on('click', function () {
        $(this).toggleClass('active');
        $('.menu').toggleClass('active');
        sizes();
    });
    $('.shop-block__categories-item').on('click', function () {
        $('.shop-block__categories-item').removeClass('active');
        $(this).addClass('active');
    });
    $('.site-block__head-arrow').on('click', function () {
        $(this).toggleClass('active');
        $(this).parent().parent().parent().siblings($('.profile__address-list-body')).slideToggle();
    });
    $('.fancybox-link').fancybox({
        arrows : false,
        dragToClose: false,
        opacity: 0.2,
    });
    $('.fancybox-link').on('click', popupSliders);
    $('.popup-no-close').on('click', function (e) {
        e.stopPropagation();
    });
    $('.header__notifications-body').on('click', function (e) {
        e.stopPropagation();
    });
    $('.popup-orders').on('click', function (e) {
        $.fancybox.close();
    });
    $('.header__notifications').on('click', function (e) {
        $(this).toggleClass('active');
        e.stopPropagation();
    });
    if ($(window).width() < 768) {
        $('.support-faq__tools-item').on('click', function () {
            $('.support-faq__tools-item-bottom').not('.support-faq__tools-item.active .support-faq__tools-item-bottom').slideUp();
            $(this).children('.support-faq__tools-item-bottom').slideToggle();
        });
    }
    $('.promo-main__slider').slick({
        infinite: false,
        dots: true,
        arrows: false,
        fade: true,
        slidesToShow: 1,
        slidesToScroll: 1,
        variableWidth: false,
    });
    function imageProportion(currentElement, proportion) {
        $(currentElement).each(function () {
            $(this).height($(this).width() / proportion);
        });
    }
    imageProportion('.promo-main__slider-item', 2.668);
    imageProportion('.video-list__item-img', 1.703);
    function popupSliders() {
        $('.product-card__slider-small').slick({
            infinite: false,
            dots: false,
            arrows: false,
            slidesToShow: 3,
            slidesToScroll: 1,
            variableWidth: false,
            focusOnSelect: true,
            asNavFor: '.product-card__slider-big',
            responsive: [
                {
                    breakpoint: 1399,
                    settings: {
                        variableWidth: false
                    }
                },
            ]
        });
        $('.product-card__slider-big').slick({
            infinite: false,
            dots: false,
            arrows: false,
            slidesToShow: 1,
            slidesToScroll: 1,
            variableWidth: false,
            asNavFor: '.product-card__slider-small',
        });
    }
    $("input[type='tel']").mask("+7 (999) 999-99-99");
});