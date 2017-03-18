(function($) {
    var clock
    $(function() {

        $('.button-collapse').sideNav();
        $('.tooltipped').tooltip({
            delay: 50
        });
        $('.modal').modal();
        $('select').material_select();
        $('.collapsible').collapsible();
        var clock;

        clock = $('.clock').FlipClock({
            clockFace: 'DailyCounter',
            autoStart: false,
        });

        clock.setTime(220880);
        clock.setCountdown(true);
        clock.start();
    }); // end of document ready
})(jQuery); // end of jQuery name space