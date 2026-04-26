(function($) {
    'use strict';

    var pricingTable = {};
    mkdf.modules.pricingTable = pricingTable;

    pricingTable.mkdfInitPricingTable = mkdfInitPricingTable;


    pricingTable.mkdfOnDocumentReady = mkdfOnDocumentReady;

    $(document).ready(mkdfOnDocumentReady);
    $(window).on('load', mkdfOnWindowLoad);

    /*
     All functions to be called on $(document).ready() should be in this function
     */
    function mkdfOnDocumentReady() {
        mkdfInitPricingTable();
    }

    /**
	 All functions to be called on $(window).on('load') should be in this function
     */
    function mkdfOnWindowLoad() {
        mkdfElementorPricingTable();
    }

    /**
     * Elementor
     */
    function mkdfElementorPricingTable(){
        $(window).on('elementor/frontend/init', function () {
            elementorFrontend.hooks.addAction( 'frontend/element_ready/mkdf_pricing_table.default', function() {
                mkdfInitPricingTable();
            } );
        });
    }

    /**
     * Init Pricing Table badge animation
     */
    function mkdfInitPricingTable() {
        var pricingTables = $('.mkdf-pricing-tables');

        if(pricingTables.length) {
            pricingTables.each(function () {
                pricingTables.appear(function() {
                    pricingTables.find('.mkdf-active-text').addClass('active');
                },{accX: 0, accY: mkdfGlobalVars.vars.mkdfElementAppearAmount});
            });
        }
    }

})(jQuery);
