// INSPINIA Landing Page Custom scripts
$(document).ready(function () {

    // Highlight the top nav as scrolling
    $('body').scrollspy({
        target: '.navbar-fixed-top',
        offset: 80
    })

    // Page scrolling feature
    $('a.page-scroll').bind('click', function(event) {
        var link = $(this);
        $('html, body').stop().animate({
            scrollTop: $(link.attr('href')).offset().top - 70
        }, 500);
        event.preventDefault();
    });
    $(".nav-tabs a").click(function(){
        $(this).tab('show');
    });

});
$(".list-group li").hover(function(){
    $(".listshow a").show("normal");
},);
$(".list-group li").mouseleave(function(){
    $(".listshow a").hide("normal");
});
// Activate WOW.js plugin for animation on scrol
// new WOW().init();