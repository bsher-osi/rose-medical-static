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