/**
 * Init Elliptical slider shortcode
 */

(function($) {
	'use strict';

	var ellipticalSlider = {};
	mkdf.modules.ellipticalSlider = ellipticalSlider;

	ellipticalSlider.mkdfInitEllipticalSlider = mkdfInitEllipticalSlider;


	ellipticalSlider.mkdfOnDocumentReady = mkdfOnDocumentReady;

	$(document).ready(mkdfOnDocumentReady);
	$(window).on('load', mkdfOnWindowLoad);

	/*
	 All functions to be called on $(document).ready() should be in this function
	 */
	function mkdfOnDocumentReady() {
		mkdfInitEllipticalSlider();
	}

	/**
	 All functions to be called on $(document).ready() should be in this function
	 */
	function mkdfOnWindowLoad() {
		mkdfElementorEllipticalSlider();
	}

	/**
	 * Elementor
	 */
	function mkdfElementorEllipticalSlider() {
		$(window).on('elementor/frontend/init', function () {
			elementorFrontend.hooks.addAction('frontend/element_ready/mkdf_elliptical_slider.default', function () {
				mkdfInitEllipticalSlider();
			});
		});
	}

	/*
	 **	Init Elliptical slider shortcode
	 */
	function mkdfInitEllipticalSlider(){

		var ellipticalSliders = $('.mkdf-elliptical-slider');
		if(ellipticalSliders.length){
			ellipticalSliders.each(function(){

				var thisEllipticalSlider = $(this);

				var interval = 5000;
				var controlNav = true;
				var directionNav = false;
				var animationSpeed = 600;
				var animationLoop = true;

				if(typeof thisEllipticalSlider.data('animation-speed') !== 'undefined' && thisEllipticalSlider.data('animation-speed') !== false) {
					animationSpeed = thisEllipticalSlider.data('animation-speed');
				}

				thisEllipticalSlider.flexslider({
					selector: ".mkdf-elliptical-slider-slides > .mkdf-elliptical-slide",
					animationLoop: animationLoop,
					controlNav: controlNav,
					directionNav: directionNav,
					useCSS: false,
					pauseOnAction: false,
					pauseOnHover: false,
					slideshow: true,
					animationSpeed: animationSpeed,
					slideshowSpeed: interval,
					touch: true
				});
			});

		}

	}

})(jQuery);

