// Set tabs
$(document).ready(function(){
    $('.tabs').click(function(){
        $('.tabs').removeClass('active-tabs');
        $(this).addClass('active-tabs');
    });
});

// Tabs events
$(document).ready(function(){
    $('.tabs').click(function(){
        // Remove 'active-tabs' class from all tabs
        $('.tabs').removeClass('active-tabs');
        // Add 'active-tabs' class to clicked tab
        $(this).addClass('active-tabs');
        $('.tab-content').hide();
        var tab = $(this).attr('data-tab');
        $('#' + tab).show();
    });
});