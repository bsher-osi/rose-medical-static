(function($) {
	'use strict';

	var team = {};
	mkdf.modules.team = team;

	team.mkdfBookingForm = mkdfBookingForm;


	team.mkdfOnDocumentReady = mkdfOnDocumentReady;

	$(document).ready(mkdfOnDocumentReady);

	/*
	 All functions to be called on $(document).ready() should be in this function
	 */
	function mkdfOnDocumentReady() {
		mkdfBookingForm();
	}


	/**
	 * Testimonials Shortcode
	 */

function mkdfBookingForm() {
	var bookNow = $('.mkdf-book-now');
	bookNow.each(function() {
		var book = $(this);

		book.on('click',function(){
			$(".mkdf-booking-form ").slideToggle();
		});

	})

	var bookingForms = $('.mkdf-booking-form');
	bookingForms.each(function(index) {
		var form = $(this);
		var formItself = form.find('form');
		var responseDiv = formItself.find('.mkdf-bf-form-response-holder');
		var workDays = form.data('workdays');
		var startTime = form.data('start-time');
		var endTime = form.data('end-time');
		var bookingPeriod = form.data('period');

		var timesArray = [];
		for(var xh=startTime;xh<=endTime-1;xh++){
			for(var xm=0;xm<60;xm+=bookingPeriod){
				var time = ("0"+xh).slice(-2)+':'+("0"+xm).slice(-2);
				timesArray.push(time);
			}
		}

		
		form.find('.mkdf-bf-input-date').datetimepicker({
			timepicker: false,
			minDate: 0,
			format: 'Y-m-d',
			disabledWeekDays: workDays
		});
		form.find('.mkdf-bf-input-time').datetimepicker({
			datepicker: false,
			allowTimes: timesArray,
			step: bookingPeriod,
			format: 'H:i'
		});

		formItself.submit(function(e) {
			e.preventDefault();

			var enquiryData = {
				doctor: formItself.find('input.mkdf-bf-input-doctor').val(),
				date: formItself.find('input.mkdf-bf-input-date').val(),
				time: formItself.find('input.mkdf-bf-input-time').val(),
				name: formItself.find('input.mkdf-bf-input-name').val(),
				contact: formItself.find('input.mkdf-bf-input-contact').val(),
				message: formItself.find('textarea.mkdf-bf-input-request').val(),
				nonce: formItself.find('.nonce input:first-child').val()
			};

			var requestData = {
				action: 'mkdf_action_send_booking_form',
				data: enquiryData
			};


			$.ajax({
				type: 'POST',
				data: requestData,
				url: MikadoAjaxUrl,
				success: function( response ) {
					responseDiv.html(response.data).slideDown(300);
					setTimeout(function() {
						responseDiv.slideUp(300, function() {
							responseDiv.html('');
						});
					}, 3000);
				}
			});
		});
	});
}
})(jQuery);
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