// Set tabs
$(document).ready(function(){
    $('.tabs').click(function(){
        $('.tabs').removeClass('active-tabs');
        $(this).addClass('active-tabs');
    });
});

// Tabs events
// $(document).ready(function(){
//     $('.tabs').click(function(){
//         $('.tabs').removeClass('active-tabs');
//         $(this).addClass('active-tabs');
//         $('.tab-content').hide();
//         var tab = $(this).attr('data-tab');
//         $('#' + tab).show();
//     });
// });