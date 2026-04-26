(function($) {
    "use strict";

    var title = {};
    mkdf.modules.title = title;

    title.mkdfOnDocumentReady = mkdfOnDocumentReady;
    title.mkdfOnWindowResize = mkdfOnWindowResize;

    $(document).ready(mkdfOnDocumentReady);
    $(window).resize(mkdfOnWindowResize);
    
    /* 
        All functions to be called on $(document).ready() should be in this function
    */
    function mkdfOnDocumentReady() {
	    initTitleFullHeight();
	    mkdfParallaxTitle();
    }

    /* 
        All functions to be called on $(window).resize() should be in this function
    */
    function mkdfOnWindowResize() {
	    initTitleFullHeight();
    }

    /*
     **	Title image with parallax effect
     */
    function mkdfParallaxTitle(){
	    var parallaxBackground = $('.mkdf-title.mkdf-has-parallax-background');
	    
        if(parallaxBackground.length > 0 && $('.touch').length === 0){
            var parallaxBackgroundWithZoomOut = $('.mkdf-title.mkdf-has-parallax-background.mkdf-zoom-out');

            var backgroundSizeWidth = parseInt(parallaxBackground.data('background-width').match(/\d+/));
            var titleHolderHeight = parallaxBackground.data('height');
            var titleRate = (titleHolderHeight / 10000) * 7;
            var titleYPos = -(mkdf.scroll * titleRate);

            //set position of background on doc ready
            parallaxBackground.css({'background-position': 'center '+ (titleYPos+mkdfGlobalVars.vars.mkdfAddForAdminBar) +'px' });
            parallaxBackgroundWithZoomOut.css({'background-size': backgroundSizeWidth-mkdf.scroll + 'px auto'});

            //set position of background on window scroll
            $(window).scroll(function() {
                titleYPos = -(mkdf.scroll * titleRate);
                parallaxBackground.css({'background-position': 'center ' + (titleYPos+mkdfGlobalVars.vars.mkdfAddForAdminBar) + 'px' });
                parallaxBackgroundWithZoomOut.css({'background-size': backgroundSizeWidth-mkdf.scroll + 'px auto'});
            });
        }
    }
	
	function initTitleFullHeight() {
		var title = $('.mkdf-title');
		
		if(title.length > 0 && title.hasClass('mkdf-title-full-height')) {
			var titleHolder = title.find('.mkdf-title-holder');
			var titleMargin = parseInt($('.mkdf-content').css('margin-top'));
			var titleHolderPadding = parseInt(titleHolder.css('padding-top'));
			if(mkdf.windowWidth > 1024) {
				if(titleMargin < 0) {
					title.css("height", mkdf.windowHeight);
					title.attr("data-height", mkdf.windowHeight);
					titleHolder.css("height", mkdf.windowHeight);
					if(titleHolderPadding > 0) {
						titleHolder.css("height", mkdf.windowHeight - mkdfGlobalVars.vars.mkdfMenuAreaHeight);
					}
				} else {
					title.css("height", mkdf.windowHeight - mkdfGlobalVars.vars.mkdfMenuAreaHeight);
					title.attr("data-height", mkdf.windowHeight - mkdfGlobalVars.vars.mkdfMenuAreaHeight);
					titleHolder.css("height", mkdf.windowHeight - mkdfGlobalVars.vars.mkdfMenuAreaHeight);
				}
			} else {
				title.css("height", mkdf.windowHeight - mkdfGlobalVars.vars.mkdfMobileHeaderHeight);
				title.attr("data-height", mkdf.windowHeight - mkdfGlobalVars.vars.mkdfMobileHeaderHeight);
				titleHolder.css("height", mkdf.windowHeight - mkdfGlobalVars.vars.mkdfMobileHeaderHeight);
			}
		}
	}

})(jQuery);
