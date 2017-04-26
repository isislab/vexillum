(function($) {
    $(function() {

        $('.button-collapse').sideNav();
        $('.modal').modal();
        $('select').material_select();
        $('.collapsible').collapsible();
        if (typeof updatetext !== 'undefined') {
        	$('#modal4').click(updatetext());
    	}
    	if (typeof clockinit !== 'undefined') {
        	clockinit();
        }
        if (typeof tokentip !== 'undefined'){
        	tokentip();
        }else{
        	$('.tooltipped').tooltip({
            delay: 50
        	});
        }

    }); // end of document ready
})(jQuery); // end of jQuery name space