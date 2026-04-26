(function($) {
    'use strict';

    var testimonials = {};
    mkdf.modules.testimonials = testimonials;

    testimonials.mkdfInitTestimonials = mkdfInitTestimonials;


    testimonials.mkdfOnDocumentReady = mkdfOnDocumentReady;

    $(document).ready(mkdfOnDocumentReady);

    /*
     All functions to be called on $(document).ready() should be in this function
     */
    function mkdfOnDocumentReady() {
        mkdfInitTestimonials();
    }


    /**
     * Testimonials Shortcode
     */

    function mkdfInitTestimonials(){

        var testimonial = $('.mkdf-owl-testimonials');
        if (testimonial.length) {
            testimonial.each(function () {

                var theseTestimonials = $(this).filter(':not(.mkdf-single-testimonial)'),
                    testimonialsHolder = $(this).closest('.mkdf-testimonials-holder'),
                    numberOfItems,
                    numberOfItemsTablet,
                    numberOfItemsMobile,
                    numberOfItemsLaptop,
                    itemMargin,
                    animationSpeed = 400,
                    dragGrab,
                    touchDrag = true,
                    allowFlag = true,
                    dotsNavigation = false,
                    arrowsNavigation = false;

                // slider
                if (theseTestimonials.hasClass('mkdf-testimonials-slider')) {
                    numberOfItems = 1;
                    numberOfItemsLaptop = 1;
                    numberOfItemsTablet = 1;
                    numberOfItemsMobile = 1;
                    itemMargin = 0;
                    dragGrab = false;
                    touchDrag = false;
                }

                // carousel
                if (theseTestimonials.hasClass('mkdf-testimonials-carousel')) {
                    if (typeof theseTestimonials.data('visible-items') !== 'undefined' && theseTestimonials.data('visible-items') !== false) {
                        numberOfItems = theseTestimonials.data('visible-items');
                    }
                    else {
                        numberOfItems = 3;
                    }
                    numberOfItemsLaptop = 3;
                    numberOfItemsTablet = 2;
                    numberOfItemsMobile = 1;
                    itemMargin = 34;
                    dragGrab = true;
                }

                // get animation speed
                if (theseTestimonials.hasClass('mkdf-testimonials-slider')) {
                    animationSpeed = 850;
                }
                if (typeof theseTestimonials.data('animation-speed') !== 'undefined' && theseTestimonials.data('animation-speed') !== false) {
                    animationSpeed = theseTestimonials.data('animation-speed');
                }

                if (theseTestimonials.hasClass('mkdf-testimonials-navigation')) {

                    // Go to the next item
                    theseTestimonials.parent().parent().parent().find('.mkdf-tes-nav-next').on('click',function (e) {
                        e.preventDefault();
                        if(allowFlag) {

                            allowFlag = false;
                            owl.trigger('next.owl.carousel');

                            // only for slider
                            if (theseTestimonials.hasClass('mkdf-testimonials-slider')) {
                                owlImageDots.trigger('next.owl.carousel');
                            }

                            setTimeout(function(){
                                allowFlag = true;
                            }, 900);
                        }

                    });
                    // Go to the previous item
                    theseTestimonials.parent().parent().parent().find('.mkdf-tes-nav-prev').on('click',function (e) {
                        e.preventDefault();
                        if(allowFlag) {

                            allowFlag = false;
                            owl.trigger('prev.owl.carousel');

                            // only for slider
                            if (theseTestimonials.hasClass('mkdf-testimonials-slider')) {
                                owlImageDots.trigger('prev.owl.carousel');
                            }

                            setTimeout(function(){
                                allowFlag = true;
                            }, 900);
                        }
                    });
                }

                if (theseTestimonials.hasClass('mkdf-testimonials-pagination')) {
                    theseTestimonials.parent().parent().parent().find('.mkdf-tes-dot').on('click',function (e) {
                        var bullet = $(this);
                        owl.trigger('to.owl.carousel', [bullet.index(), 0, true]);
                        bullet.siblings().removeClass('active');
                        bullet.addClass('active');


                        if (theseTestimonials.hasClass('mkdf-testimonials-slider')) {
                            owlImageDots.trigger('to.owl.carousel', [bullet.index(), 0, true]);
                        }
                    });
                }

                if (theseTestimonials.hasClass('mkdf-testimonials-light')) {
                    theseTestimonials.parent().parent().parent().find('.mkdf-tes-nav').addClass('light');
                }

                if (theseTestimonials.hasClass('mkdf-testimonials-dark')) {
                    theseTestimonials.parent().parent().parent().find('.mkdf-tes-nav').addClass('dark');
                }

                // get navigation
                var autoplay = true;
                var enableLoop = true;
                var sliderSpeed = 5000;


                if( testimonial.data('enable-autoplay')== 'no'){
                    autoplay = false;
                }

                if( testimonial.data('enable-loop')== 'no'){
                    enableLoop = false;
                }

                if( testimonial.data('enable-pagination')== 'yes'){
                    dotsNavigation = true;
                }

                if( testimonial.data('enable-navigation')== 'yes'){
                    arrowsNavigation = true;
                }

                if( testimonial.data('slider-speed') !== ''){
                    sliderSpeed = testimonial.data('slider-speed');
                }

                var owl = theseTestimonials.owlCarousel({
                    responsiveClass: true,
                    responsive: {
                        0: {
                            items: numberOfItemsMobile
                        },
                        768: {
                            items: numberOfItemsTablet
                        },
                        1260: {
                            items: numberOfItemsLaptop
                        },
                        1441: {
                            items: numberOfItems
                        }
                    },
                    margin: itemMargin,
                    autoplay: autoplay,
                    autoplayTimeout: sliderSpeed,
                    smartSpeed: animationSpeed,
                    loop: enableLoop,
                    info: true,
                    dots: dotsNavigation,
                    nav: false,
                    mouseDrag: dragGrab,
                    touchDrag: touchDrag,
                    autoplayHoverPause: false,
                    onInitialized: function () {
                        mkdfAppear();
                    }

                });

                if (theseTestimonials.hasClass('mkdf-testimonials-slider')) {
                    owl.on('changed.owl.carousel', function (event) {
                        owlImageDots.trigger('to.owl.carousel', [event.item.index - 3, 0, true]);
                    });
                }

                // callback function to show testimonials
                function mkdfAppear() {
                    testimonialsHolder.css('visibility', 'visible');
                    testimonialsHolder.animate({opacity: 1}, 300);
                }


                //carousel additional image slider
                if (theseTestimonials.hasClass('mkdf-testimonials-slider')) {
                    var imageDots = $('.mkdf-tes-image-nav');

                    var owlImageDots = imageDots.owlCarousel({
                        autoplay: autoplay,
                        autoplayTimeout: sliderSpeed,
                        smartSpeed: animationSpeed,
                        center: true,
                        loop: enableLoop,
                        mouseDrag: dragGrab,
                        autoplayHoverPause: false,
                        touchDrag: touchDrag,
                        responsive:{
                            480:{
                                items:3
                            },
                            0:{
                                items:1
                            }
                        }
                    });

                }
            });

            mkdf.modules.common.mkdfInitParallax;
        }
    }
})(jQuery);