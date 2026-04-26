(function($) {
	'use strict';
	
	var process = {};
	mkdf.modules.process = process;

	process.mkdfInitProcessAnimation = mkdfInitProcessAnimation;


	process.mkdfOnDocumentReady = mkdfOnDocumentReady;
	
	$(document).ready(mkdfOnDocumentReady);
	$(window).on('load', mkdfOnWindowLoad);
	
	/*
	 All functions to be called on $(document).ready() should be in this function
	 */
	function mkdfOnDocumentReady() {
		mkdfInitProcessAnimation();
	}

	/**
	 All functions to be called on $(document).ready() should be in this function
	 */
	function mkdfOnWindowLoad() {
		mkdfElementorProcess();
	}

	/**
	 * Elementor
	 */
	function mkdfElementorProcess() {
		$(window).on('elementor/frontend/init', function () {
			elementorFrontend.hooks.addAction('frontend/element_ready/mkdf_process.default', function () {
				mkdfInitProcessAnimation();
			});
		});
	}

	/*
	 * Process Animation
	 */
	function mkdfInitProcessAnimation() {
		var processAnimationHolders = $('.mkdf-animate-process-items-yes');

		if (processAnimationHolders.length && !mkdf.htmlEl.hasClass('touch')) {
			processAnimationHolders.appear(function(){
				var processAnimationHolder = $(this),
					processItems = processAnimationHolder.find('.mkdf-process-item-holder'),
					processBgrnd = processAnimationHolder.find('.mkdf-process-bg-holder');

				processItems.each(function(i){
					var currentItem = $(this);

					setTimeout(function(){
						currentItem.addClass('mkdf-appeared');

						if (i == processItems.length - 1) {
							processBgrnd.addClass('mkdf-appeared');
						}
					}, i*200);
				});
			},{accX: 0, accY: mkdfGlobalVars.vars.mkdfElementAppearAmount});
		}
	}
	
})(jQuery);