(function($) {
	'use strict';
	
	var tabs = {};
	mkdf.modules.tabs = tabs;
	
	tabs.mkdfInitTabs = mkdfInitTabs;
	tabs.mkdfInitTabIcons =mkdfInitTabIcons;
	tabs.mkdfTabsNavUnderline = mkdfTabsNavUnderline;

	
	tabs.mkdfOnDocumentReady = mkdfOnDocumentReady;
	tabs.mkdfOnWindowLoad = mkdfOnWindowLoad;
	
	$(document).ready(mkdfOnDocumentReady);
	$(window).on('load', mkdfOnWindowLoad);
	
	/*
	 All functions to be called on $(document).ready() should be in this function
	 */
	function mkdfOnDocumentReady() {
		mkdfInitTabs();
		mkdfInitTabIcons();
	}

	/*
	 All functions to be called on $(window).load() should be in this function
	 */
	function mkdfOnWindowLoad() {
		mkdfTabsNavUnderline();
		mkdfElementorIconTabs();
	}

	/**
	 * Elementor
	 */
	function mkdfElementorIconTabs(){
		$(window).on('elementor/frontend/init', function () {
			elementorFrontend.hooks.addAction( 'frontend/element_ready/mkdf_icon_tabs.default', function() {
				mkdfInitTabs();
				mkdfInitTabIcons();
			} );
		});
	}
	
	/*
	 **	Init tabs shortcode
	 */
	function mkdfInitTabs(){
		var tabs = $('.mkdf-icon-tabs');
		
		if(tabs.length){
			tabs.each(function(){
				var thisTabs = $(this);
				
				thisTabs.children('.mkdf-icon-tab-container').each(function(index){
					index = index + 1;
					var that = $(this),
						link = that.attr('id'),
						navItem = that.parent().find('.mkdf-icon-tabs-nav li:nth-child('+index+') a'),
						navLink = navItem.attr('href');
					
					link = '#'+link;
					
					if(link.indexOf(navLink) > -1) {
						navItem.attr('href',link);
					}
				});
				
				thisTabs.tabs();
			});
		}
	}

	/*
	 **	Generate icons in tabs navigation
	 */
	function mkdfInitTabIcons(){

		var tabContent = $('.mkdf-icon-tab-container');
		if(tabContent.length){

			tabContent.each(function(){
				var thisTabContent = $(this);

				var id = thisTabContent.attr('id');
				var icon = '';
				if(typeof thisTabContent.data('icon-html') !== 'undefined' || thisTabContent.data('icon-html') !== 'false') {
					icon = thisTabContent.data('icon-html');
				}

				var tabNav = thisTabContent.parents('.mkdf-icon-tabs').find('.mkdf-icon-tabs-nav > li > a[href="#'+id+'"]');

				if(typeof(tabNav) !== 'undefined') {
					tabNav.prepend(icon);
				}
			});
		}
	}

	function mkdfTabsNavUnderline() {
		var tabs = $('.mkdf-icon-tabs');

		if(tabs.length) {
			tabs.each(function(){
				var tabNav = $(this),
					tabNavs = tabNav.find('.mkdf-icon-tabs-nav'),
					navItemActive = tabNavs.find('.ui-state-active'),
					navLine = tabNav.find('.mkdf-tabs-nav-line'),
					navItems = tabNavs.find('> li');

				var navLineParams = function() {
					var navItemActive = tabNavs.find('.ui-state-active');
					navLine.css('width', navItemActive.outerWidth() - 60);
					navLine.css('left', navItemActive.offset().left - tabNavs.offset().left + 30);
					navLine.css('opacity', 1);
				};

				if( navItemActive.length ) {
					navLineParams();
				} else {
					navLine.css('left', navItems.first().offset().left - tabNavs.offset().left + 30);
				}

				navItems.each(function(){
					var navItem = $(this),
						navItemWidth = navItem.outerWidth() - 60,
						navMenuOffset = tabNavs.offset().left,
						navItemOffset = navItem.offset().left - navMenuOffset + 30;

					navItem.mouseenter(function(){
						navLine.css('width', navItemWidth);
						navLine.css('left', navItemOffset);
					});
				});

				tabNavs.mouseleave(function(){
					navLineParams();
				});
			});
		}

	}
	
})(jQuery);