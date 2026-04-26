(function($) {
	"use strict";
	
	var header = {};
	mkdf.modules.header = header;
	
	header.mkdfSetDropDownMenuPosition     = mkdfSetDropDownMenuPosition;
	header.mkdfSetDropDownWideMenuPosition = mkdfSetDropDownWideMenuPosition;
	
	header.mkdfOnDocumentReady = mkdfOnDocumentReady;
	header.mkdfOnWindowLoad = mkdfOnWindowLoad;
	header.mkdfOnWindowResize = mkdfOnWindowResize;
	header.mkdfOnWindowScroll = mkdfOnWindowScroll;
	
	$(document).ready(mkdfOnDocumentReady);
	$(window).on('load', mkdfOnWindowLoad);
	$(window).resize(mkdfOnWindowResize);
	$(window).scroll(mkdfOnWindowScroll);
	
	/*
	 All functions to be called on $(document).ready() should be in this function
	 */
	function mkdfOnDocumentReady() {
		mkdfSetDropDownMenuPosition();
		mkdfDropDownMenu();
		mkdfSearch();
		mkdfSideArea();
		mkdfSideAreaScroll();
		mkdfMenuUnderline();
	}
	
	/*
	 All functions to be called on $(window).load() should be in this function
	 */
	function mkdfOnWindowLoad() {
		mkdfSetDropDownWideMenuPosition();
	}
	
	/*
	 All functions to be called on $(window).resize() should be in this function
	 */
	function mkdfOnWindowResize() {
	}
	
	/*
	 All functions to be called on $(window).scroll() should be in this function
	 */
	function mkdfOnWindowScroll() {
	}
	
	/**
	 * Set dropdown position
	 */
	function mkdfSetDropDownMenuPosition() {
		var menuItems = $('.mkdf-drop-down > ul > li.narrow.menu-item-has-children');
		
		if (menuItems.length) {
			menuItems.each(function (i) {
				var thisItem = $(this),
					menuItemPosition = thisItem.offset().left,
					dropdownHolder = thisItem.find('.second'),
					dropdownMenuItem = dropdownHolder.find('.inner ul'),
					dropdownMenuWidth = dropdownMenuItem.outerWidth(),
					menuItemFromLeft = mkdf.windowWidth - menuItemPosition;
				
				if (mkdf.body.hasClass('mkdf-boxed')) {
					menuItemFromLeft = mkdf.boxedLayoutWidth - (menuItemPosition - (mkdf.windowWidth - mkdf.boxedLayoutWidth ) / 2);
				}
				
				var dropDownMenuFromLeft; //has to stay undefined beacuse 'dropDownMenuFromLeft < dropdownMenuWidth' condition will be true
				
				if (thisItem.find('li.sub').length > 0) {
					dropDownMenuFromLeft = menuItemFromLeft - dropdownMenuWidth;
				}
				
				dropdownHolder.removeClass('right');
				dropdownMenuItem.removeClass('right');
				if (menuItemFromLeft < dropdownMenuWidth || dropDownMenuFromLeft < dropdownMenuWidth) {
					dropdownHolder.addClass('right');
					dropdownMenuItem.addClass('right');
				}
			});
		}
	}
	
	/**
	 * Set dropdown wide position
	 */
	function mkdfSetDropDownWideMenuPosition(){
		var menuItems = $(".mkdf-drop-down > ul > li.wide");
		
		if(menuItems.length) {
			menuItems.each( function(i) {
				var menuItemSubMenu = $(menuItems[i]).find('.second');
				
				if(menuItemSubMenu.length && !menuItemSubMenu.hasClass('left_position') && !menuItemSubMenu.hasClass('right_position')) {
					menuItemSubMenu.css('left', 0);
					
					var left_position = menuItemSubMenu.offset().left;
					
					if(mkdf.body.hasClass('mkdf-boxed')) {
						var boxedWidth = $('.mkdf-boxed .mkdf-wrapper .mkdf-wrapper-inner').outerWidth();
						left_position = left_position - (mkdf.windowWidth - boxedWidth) / 2;
						
						menuItemSubMenu.css('left', -left_position);
						menuItemSubMenu.css('width', boxedWidth);
					} else {
						menuItemSubMenu.css('left', -left_position);
						menuItemSubMenu.css('width', mkdf.windowWidth);
					}
				}
			});
		}
	}
	
	function mkdfDropDownMenu() {
		var menu_items = $('.mkdf-drop-down > ul > li');
		
		menu_items.each(function(i) {
			if($(menu_items[i]).find('.second').length > 0) {
				var thisItem = $(menu_items[i]),
					dropDownSecondDiv = thisItem.find('.second');
				
				if(thisItem.hasClass('wide')) {
					//set columns to be same height - start
					var tallest = 0,
						dropDownSecondItem = $(this).find('.second > .inner > ul > li');
					
					dropDownSecondItem.each(function() {
						var thisHeight = $(this).height();
						if(thisHeight > tallest) {
							tallest = thisHeight;
						}
					});
					
					dropDownSecondItem.css('height', ''); // delete old inline css - via resize
					dropDownSecondItem.height(tallest);
					//set columns to be same height - end
				}
				
				if(!mkdf.menuDropdownHeightSet) {
					thisItem.data('original_height', dropDownSecondDiv.height() + 'px');
					dropDownSecondDiv.height(0);
				}
				
				if(navigator.userAgent.match(/(iPod|iPhone|iPad)/)) {
					thisItem.on("touchstart mouseenter", function() {
						dropDownSecondDiv.css({
							'height': thisItem.data('original_height'),
							'overflow': 'visible',
							'visibility': 'visible',
							'opacity': '1'
						});
					}).on("mouseleave", function() {
						dropDownSecondDiv.css({
							'height': '0px',
							'overflow': 'hidden',
							'visibility': 'hidden',
							'opacity': '0'
						});
					});
				} else {
					if(mkdf.body.hasClass('mkdf-dropdown-animate-height')) {
						thisItem.mouseenter(function() {
							dropDownSecondDiv.css({
								'visibility': 'visible',
								'height': '0px',
								'opacity': '0'
							});
							dropDownSecondDiv.stop().animate({
								'height': thisItem.data('original_height'),
								opacity: 1
							}, 300, function() {
								dropDownSecondDiv.css('overflow', 'visible');
							});
						}).mouseleave(function() {
							dropDownSecondDiv.stop().animate({
								'height': '0px'
							}, 150, function() {
								dropDownSecondDiv.css({
									'overflow': 'hidden',
									'visibility': 'hidden'
								});
							});
						});
					} else {
						var config = {
							interval: 0,
							over: function() {
								setTimeout(function() {
									dropDownSecondDiv.addClass('mkdf-drop-down-start');
									dropDownSecondDiv.stop().css({'height': thisItem.data('original_height')});
								}, 150);
							},
							timeout: 150,
							out: function() {
								dropDownSecondDiv.stop().css({'height': '0px'});
								dropDownSecondDiv.removeClass('mkdf-drop-down-start');
							}
						};
						thisItem.hoverIntent(config);
					}
				}
			}
		});
		
		$('.mkdf-drop-down ul li.wide ul li a').on('click', function(e) {
			if (e.which == 1){
				var $this = $(this);
				setTimeout(function() {
					$this.mouseleave();
				}, 500);
			}
		});
		
		mkdf.menuDropdownHeightSet = true;
	}
	
	/**
	 * Init Search Types
	 */
	function mkdfSearch() {
		var searchOpener = $('a.mkdf-search-opener'),
			searchForm,
			searchClose;
		
		if ( searchOpener.length > 0 ) {
			//Check for type of search
			if ( mkdf.body.hasClass( 'mkdf-fullscreen-search' ) ) {
				searchClose = $( '.mkdf-fullscreen-search-close' );
				mkdfFullscreenSearch();
				
			} else if ( mkdf.body.hasClass( 'mkdf-slide-from-header-bottom' ) ) {
				mkdfSearchSlideFromHeaderBottom();
				
			} else if ( mkdf.body.hasClass( 'mkdf-search-covers-header' ) ) {
				mkdfSearchCoversHeader();
				
			} else if ( mkdf.body.hasClass( 'mkdf-search-slides-from-window-top' ) ) {
				searchForm = $('.mkdf-search-slide-window-top');
				searchClose = $('.mkdf-swt-search-close');
				mkdfSearchWindowTop();
			}
		}
		
		/**
		 * Fullscreen search fade
		 */
		function mkdfFullscreenSearch() {
			var searchHolder = $('.mkdf-fullscreen-search-holder');
			
			searchOpener.on('click',function (e) {
				e.preventDefault();
				
				if (searchHolder.hasClass('mkdf-animate')) {
					mkdf.body.removeClass('mkdf-fullscreen-search-opened mkdf-search-fade-out');
					mkdf.body.removeClass('mkdf-search-fade-in');
					searchHolder.removeClass('mkdf-animate');
					
					setTimeout(function () {
						searchHolder.find('.mkdf-search-field').val('');
						searchHolder.find('.mkdf-search-field').blur();
					}, 300);
					
					mkdf.modules.common.mkdfEnableScroll();
				} else {
					mkdf.body.addClass('mkdf-fullscreen-search-opened mkdf-search-fade-in');
					mkdf.body.removeClass('mkdf-search-fade-out');
					searchHolder.addClass('mkdf-animate');
					
					setTimeout(function () {
						searchHolder.find('.mkdf-search-field').focus();
					}, 900);
					
					mkdf.modules.common.mkdfDisableScroll();
				}
				
				searchClose.on('click',function (e) {
					e.preventDefault();
					mkdf.body.removeClass('mkdf-fullscreen-search-opened mkdf-search-fade-in');
					mkdf.body.addClass('mkdf-search-fade-out');
					searchHolder.removeClass('mkdf-animate');
					
					setTimeout(function () {
						searchHolder.find('.mkdf-search-field').val('');
						searchHolder.find('.mkdf-search-field').blur();
					}, 300);
					
					mkdf.modules.common.mkdfEnableScroll();
				});
				
				//Close on click away
				$(document).mouseup(function (e) {
					var container = $(".mkdf-form-holder-inner");
					
					if (!container.is(e.target) && container.has(e.target).length === 0) {
						e.preventDefault();
						mkdf.body.removeClass('mkdf-fullscreen-search-opened mkdf-search-fade-in');
						mkdf.body.addClass('mkdf-search-fade-out');
						searchHolder.removeClass('mkdf-animate');
						
						setTimeout(function () {
							searchHolder.find('.mkdf-search-field').val('');
							searchHolder.find('.mkdf-search-field').blur();
						}, 300);
						
						mkdf.modules.common.mkdfEnableScroll();
					}
				});
				
				//Close on escape
				$(document).keyup(function (e) {
					if (e.keyCode == 27) { //KeyCode for ESC button is 27
						mkdf.body.removeClass('mkdf-fullscreen-search-opened mkdf-search-fade-in');
						mkdf.body.addClass('mkdf-search-fade-out');
						searchHolder.removeClass('mkdf-animate');
						
						setTimeout(function () {
							searchHolder.find('.mkdf-search-field').val('');
							searchHolder.find('.mkdf-search-field').blur();
						}, 300);
						
						mkdf.modules.common.mkdfEnableScroll();
					}
				});
			});
			
			//Text input focus change
			var inputSearchField = $('.mkdf-fullscreen-search-holder .mkdf-search-field'),
				inputSearchLine = $('.mkdf-fullscreen-search-holder .mkdf-field-holder .mkdf-line');
			
			inputSearchField.focus(function () {
				inputSearchLine.css('width', '100%');
			});
			
			inputSearchField.blur(function () {
				inputSearchLine.css('width', '0');
			});
		}
		
		/**
		 * Search covers header type of search
		 */
		function mkdfSearchCoversHeader() {
			searchOpener.on('click',function (e) {
				e.preventDefault();
				
				var thisSearchOpener = $(this),
					searchFormHeight,
					searchFormHeaderHolder = $('.mkdf-page-header'),
					searchFormTopHeaderHolder = $('.mkdf-top-bar'),
					searchFormFixedHeaderHolder = searchFormHeaderHolder.find('.mkdf-fixed-wrapper.fixed'),
					searchFormMobileHeaderHolder = $('.mkdf-mobile-header'),
					searchForm = $('.mkdf-search-cover'),
					searchFormIsInTopHeader = !!thisSearchOpener.parents('.mkdf-top-bar').length,
					searchFormIsInFixedHeader = !!thisSearchOpener.parents('.mkdf-fixed-wrapper.fixed').length,
					searchFormIsInStickyHeader = !!thisSearchOpener.parents('.mkdf-sticky-header').length,
					searchFormIsInMobileHeader = !!thisSearchOpener.parents('.mkdf-mobile-header').length;
				
				searchForm.removeClass('mkdf-is-active');
				
				//Find search form position in header and height
				if (searchFormIsInTopHeader) {
					searchFormHeight = mkdfGlobalVars.vars.mkdfTopBarHeight;
					searchFormTopHeaderHolder.find('.mkdf-search-cover').addClass('mkdf-is-active');
					
				} else if (searchFormIsInFixedHeader) {
					searchFormHeight = searchFormFixedHeaderHolder.outerHeight();
					searchFormHeaderHolder.children('.mkdf-search-cover').addClass('mkdf-is-active');
					
				} else if (searchFormIsInStickyHeader) {
					searchFormHeight = mkdfGlobalVars.vars.mkdfStickyHeaderHeight;
					searchFormHeaderHolder.children('.mkdf-search-cover').addClass('mkdf-is-active');
					
				} else if (searchFormIsInMobileHeader) {
					if(searchFormMobileHeaderHolder.hasClass('mobile-header-appear')) {
						searchFormHeight = searchFormMobileHeaderHolder.children('.mkdf-mobile-header-inner').outerHeight();
					} else {
						searchFormHeight = searchFormMobileHeaderHolder.outerHeight();
					}
					
					searchFormMobileHeaderHolder.find('.mkdf-search-cover').addClass('mkdf-is-active');
					
				} else {
					searchFormHeight = searchFormHeaderHolder.outerHeight();
					searchFormHeaderHolder.children('.mkdf-search-cover').addClass('mkdf-is-active');
				}
				
				if(searchForm.hasClass('mkdf-is-active')) {
					searchForm.height(searchFormHeight).stop(true).fadeIn(600).find('input[type="text"]').focus();
				}
				
				searchForm.find('.mkdf-search-close').on('click',function (e) {
					e.preventDefault();
					searchForm.stop(true).fadeOut(450);
				});
				
				searchForm.blur(function () {
					searchForm.stop(true).fadeOut(450);
				});
				
				$(window).scroll(function(){
					searchForm.stop(true).fadeOut(450);
				});
			});
		}
		
		/**
		 * Search slides from window top type of search
		 */
		function mkdfSearchWindowTop() {
			searchOpener.on('click', function(e) {
				e.preventDefault();
				
				if ( searchForm.height() === 0) {
					$('.mkdf-search-slide-window-top input[type="text"]').focus();
					//Push header bottom
					mkdf.body.addClass('mkdf-search-open');
				} else {
					mkdf.body.removeClass('mkdf-search-open');
				}
				
				$(window).scroll(function() {
					if ( searchForm.height() !== 0 && mkdf.scroll > 50 ) {
						mkdf.body.removeClass('mkdf-search-open');
					}
				});
				
				searchClose.on('click',function(e){
					e.preventDefault();
					mkdf.body.removeClass('mkdf-search-open');
				});
			});
		}
		
		/**
		 * Search slide from header bottom type of search
		 */
		function mkdfSearchSlideFromHeaderBottom() {
			searchOpener.on('click', function(e) {
				e.preventDefault();
				
				var thisSearchOpener = $(this),
					searchIconPosition = parseInt(mkdf.windowWidth - thisSearchOpener.offset().left - thisSearchOpener.outerWidth());
				
				if(mkdf.body.hasClass('mkdf-boxed') && mkdf.windowWidth > 1024) {
					searchIconPosition -= parseInt((mkdf.windowWidth - $('.mkdf-boxed .mkdf-wrapper .mkdf-wrapper-inner').outerWidth()) / 2);
				}
				
				var searchFormHeaderHolder = $('.mkdf-page-header'),
					searchFormTopOffset = '100%',
					searchFormTopHeaderHolder = $('.mkdf-top-bar'),
					searchFormFixedHeaderHolder = searchFormHeaderHolder.find('.mkdf-fixed-wrapper.fixed'),
					searchFormMobileHeaderHolder = $('.mkdf-mobile-header'),
					searchForm = $('.mkdf-slide-from-header-bottom-holder'),
					searchFormIsInTopHeader = !!thisSearchOpener.parents('.mkdf-top-bar').length,
					searchFormIsInFixedHeader = !!thisSearchOpener.parents('.mkdf-fixed-wrapper.fixed').length,
					searchFormIsInStickyHeader = !!thisSearchOpener.parents('.mkdf-sticky-header').length,
					searchFormIsInMobileHeader = !!thisSearchOpener.parents('.mkdf-mobile-header').length;
				
				searchForm.removeClass('mkdf-is-active');
				
				//Find search form position in header and height
				if (searchFormIsInTopHeader) {
					searchFormTopHeaderHolder.find('.mkdf-slide-from-header-bottom-holder').addClass('mkdf-is-active');
					
				} else if (searchFormIsInFixedHeader) {
					searchFormTopOffset = searchFormFixedHeaderHolder.outerHeight() + mkdfGlobalVars.vars.mkdfAddForAdminBar;;
					searchFormHeaderHolder.children('.mkdf-slide-from-header-bottom-holder').addClass('mkdf-is-active');
					
				} else if (searchFormIsInStickyHeader) {
					searchFormTopOffset = mkdfGlobalVars.vars.mkdfStickyHeaderHeight + mkdfGlobalVars.vars.mkdfAddForAdminBar;;
					searchFormHeaderHolder.children('.mkdf-slide-from-header-bottom-holder').addClass('mkdf-is-active');
					
				} else if (searchFormIsInMobileHeader) {
					if(searchFormMobileHeaderHolder.hasClass('mobile-header-appear')) {
						searchFormTopOffset = searchFormMobileHeaderHolder.children('.mkdf-mobile-header-inner').outerHeight() + mkdfGlobalVars.vars.mkdfAddForAdminBar;
					}
					searchFormMobileHeaderHolder.find('.mkdf-slide-from-header-bottom-holder').addClass('mkdf-is-active');
					
				} else {
					searchFormHeaderHolder.children('.mkdf-slide-from-header-bottom-holder').addClass('mkdf-is-active');
				}
				
				if(searchForm.hasClass('mkdf-is-active')) {
					searchForm.css({'right': searchIconPosition, 'top': searchFormTopOffset}).stop(true).slideToggle(300, 'easeOutBack');
				}
				
				//Close on escape
				$(document).keyup(function(e){
					if (e.keyCode == 27 ) { //KeyCode for ESC button is 27
						searchForm.stop(true).fadeOut(0);
					}
				});
				
				$(window).scroll(function(){
					searchForm.stop(true).fadeOut(0);
				});
			});
		}
	}
	
	/**
	 * Show/hide side area
	 */
	function mkdfSideArea() {
		
		var wrapper = $('.mkdf-wrapper'),
			sideMenuButtonOpen = $('a.mkdf-side-menu-button-opener'),
			cssClass = 'mkdf-right-side-menu-opened';
		
		wrapper.prepend('<div class="mkdf-cover"/>');
		
		$('a.mkdf-side-menu-button-opener, a.mkdf-close-side-menu').on('click', function(e) {
			e.preventDefault();
			
			if(!sideMenuButtonOpen.hasClass('opened')) {
				
				sideMenuButtonOpen.addClass('opened');
				mkdf.body.addClass(cssClass);
				
				$('.mkdf-wrapper .mkdf-cover').on('click',function() {
					mkdf.body.removeClass('mkdf-right-side-menu-opened');
					sideMenuButtonOpen.removeClass('opened');
				});
				
				var currentScroll = $(window).scrollTop();
				$(window).scroll(function() {
					if(Math.abs(mkdf.scroll - currentScroll) > 400){
						mkdf.body.removeClass(cssClass);
						sideMenuButtonOpen.removeClass('opened');
					}
				});
			} else {
				sideMenuButtonOpen.removeClass('opened');
				mkdf.body.removeClass(cssClass);
			}
		});
	}
	
	/*
	 **  Smooth scroll functionality for Side Area
	 */
	function mkdfSideAreaScroll(){
		var sideMenu = $('.mkdf-side-menu');
		
		if(sideMenu.length){
            sideMenu.perfectScrollbar({
                wheelSpeed: 0.6,
                suppressScrollX: true
            });
		}
	}

	function mkdfMenuUnderline() {

		//first level menu
		var firstLevelMenus = $('.mkdf-main-menu > ul');

		if (firstLevelMenus.length) {
			firstLevelMenus.each(function () {
				var mainMenu = $(this);

				mainMenu.append('<li class="mkdf-main-menu-line bottom"></li>');

				var menuLine = mainMenu.find('.mkdf-main-menu-line'),
					menuItems = mainMenu.find('> li.menu-item'),
					initialOffset,
					scrolling = false,
					minusWidth;


				if (menuItems.filter('.mkdf-active-item').length) {
					var minusWidth = menuItems.filter('.mkdf-active-item').outerWidth() - menuItems.filter('.mkdf-active-item').find('.item_text').width();
				} else {
					var minusWidth = menuItems.first().outerWidth() - menuItems.first().find('.item_text').width();
				}


				if (menuItems.filter('.mkdf-active-item').length) {
					initialOffset = menuItems.filter('.mkdf-active-item').offset().left + minusWidth / 2;
					menuLine.css('width', menuItems.filter('.mkdf-active-item').outerWidth() - minusWidth);
				} else {
					initialOffset = menuItems.first().offset().left + minusWidth / 2;
					menuLine.css('width', menuItems.first().outerWidth() - minusWidth);
				}

				//initial positioning
				menuLine.css('left', initialOffset - mainMenu.offset().left);

				//fx on
				menuItems.mouseenter(function () {
					if (!scrolling) {
						var menuItem = $(this),
							menuItemWidth = menuItem.outerWidth() - minusWidth,
							mainMenuOffset = mainMenu.offset().left - minusWidth / 2,
							menuItemOffset = menuItem.offset().left - mainMenuOffset;

						menuLine.css('width', menuItemWidth);
						menuLine.css('left', menuItemOffset);
					}
				});

				//fx off
				mainMenu.mouseleave(function () {
					if (menuItems.filter('.mkdf-active-item').length) {
						menuLine.css('width', menuItems.filter('.mkdf-active-item').outerWidth() - minusWidth);
						initialOffset = menuItems.filter('.mkdf-active-item').offset().left + minusWidth / 2;
					} else {
						menuLine.css('width', menuItems.first().outerWidth() - minusWidth);
					}

					menuLine.css('left', initialOffset - mainMenu.offset().left);
				});
			});
		}
	}
	
})(jQuery);