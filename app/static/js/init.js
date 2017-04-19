(function($) {
    $(function() {

        $('.button-collapse').sideNav();
        $('.tooltipped').tooltip({
            delay: 50
        });
        $('.modal').modal();
        $('select').material_select();
        $('.collapsible').collapsible();
        if (typeof updatetext !== 'undefined') {
        	$('#modal4').click(updatetext());
    	}
    	if (typeof clockinit !== 'undefined') {
        	clockinit();
        }

    }); // end of document ready
})(jQuery); // end of jQuery name space