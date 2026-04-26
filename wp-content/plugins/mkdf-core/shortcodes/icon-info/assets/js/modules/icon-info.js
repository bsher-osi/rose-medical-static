(function ($) {
    'use strict';

    $(window).on('load', mkdfOnWindowLoad);    

    /*
    All functions to be called on $(window).on('load') should be in this function
    */
    function mkdfOnWindowLoad() {
        mkdfElementorIconInfo();
    }

    /**
     * Elementor
     */
    function mkdfElementorIconInfo(){
        $(window).on('elementor/frontend/init', function () {
            elementorFrontend.hooks.addAction( 'frontend/element_ready/mkdf_icon_info.default', function() {
                mkdf.modules.icon.mkdfIcon.init();
            } );
        });
    }

})(jQuery);