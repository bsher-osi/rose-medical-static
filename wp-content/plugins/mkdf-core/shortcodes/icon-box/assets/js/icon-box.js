/**
 * Init Icon box shortcode Overlapping icon type
 */

(function($) {
    'use strict';

    var iconBox = {};
    mkdf.modules.iconBox = iconBox;

    iconBox.mkdfInitIconBox = mkdfInitIconBox;

    iconBox.mkdfOnWindowLoad = mkdfOnWindowLoad;
    $(window).on('load', mkdfOnWindowLoad);

    iconBox.mkdfOnWindowResize = mkdfOnWindowResize;
    $(window).resize(mkdfOnWindowResize);

    /*
     All functions to be called on $(window).load() should be in this function
     */
    function mkdfOnWindowLoad() {
        mkdfInitIconBox();
        mkdfElementorIconBox();
    }

    /*
     All functions to be called on $(window).resize() should be in this function
     */
    function mkdfOnWindowResize() {
        mkdfInitIconBox();
    }

    /**
     * Elementor
     */
    function mkdfElementorIconBox(){
        $(window).on('elementor/frontend/init', function () {
            elementorFrontend.hooks.addAction( 'frontend/element_ready/mkdf_icon_box.default', function() {
                mkdfInitIconBox();
            } );
        });
    }

    /*
     **	Init Overlapping icon type
     */
    function mkdfInitIconBox() {

        var infoBox = $('.mkdf-icon-box-holder.overlapping-icon');

        if(infoBox.length > 0){
            infoBox.each(function(){
                var thisInfoBox = $(this);
                var contentHeight;
                var content = thisInfoBox.find('.mkdf-icon-box-content');
                var visibleInfo = thisInfoBox.find('.mkdf-icon-box-visible-content');
                var hiddenInfo = thisInfoBox.find('.mkdf-icon-box-invisible-content');
                var visibleHeight = visibleInfo.height();
                var hiddenHeight = hiddenInfo.height();
                contentHeight = visibleHeight + hiddenHeight;
                content.height(contentHeight);
                thisInfoBox.css('opacity', 1);



				thisInfoBox.on('mouseenter', function () {
				    visibleInfo.css('transform', 'translateY('+ -hiddenHeight/2 +'px)');
				});
				thisInfoBox.on('mouseleave ', function () {
					visibleInfo.css('transform', 'translateY(0)');
				});

            });
        }

    }


})(jQuery);
