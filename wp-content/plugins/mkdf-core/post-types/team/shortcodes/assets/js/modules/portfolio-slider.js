(function($) {
    'use strict';

    var teamSlider = {};
    mkdf.modules.teamSlider = teamSlider;

	teamSlider.mkdfOnWindowLoad = mkdfOnWindowLoad;

    $(window).on('load', mkdfOnWindowLoad);


    /*
     All functions to be called on $(window).on('load') should be in this function
     */
    function mkdfOnWindowLoad() {
		mkdfElementorteamSlider();
    }

	/**
	 * Elementor
	 */
	function mkdfElementorteamSlider(){
		$(window).on('elementor/frontend/init', function () {
			elementorFrontend.hooks.addAction( 'frontend/element_ready/mkdf_team_slider.default', function() {
				mkdf.modules.common.mkdfOwlSlider();
			} );
		});
	}

})(jQuery);