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

        // Hide all tab content
        $('.tab-content').hide();

        // Show content for clicked tab. Assumes each tab has a 'data-tab' attribute
        // and there are elements with class '.tab-content' and an ID that matches the 'data-tab' value
        var tab = $(this).attr('data-tab');
        $('#' + tab).show();
    });
});