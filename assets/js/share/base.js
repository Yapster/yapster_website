var ip = false;

function getBrowserWidth(){
    if (window.innerWidth){
        return window.innerWidth;}
    else if (document.documentElement && document.documentElement.clientWidth != 0){
        return document.documentElement.clientWidth;    }
    else if (document.body){return document.body.clientWidth;}
    return 0;
};

function dynamicLayout()
{

    var browserWidth = getBrowserWidth();
    if (browserWidth == 1024)
    {
        $(".responsive").removeClass("port_phone");
        $(".responsive").removeClass("port_tab");
        $(".responsive").removeClass("land_tab");
        $(".responsive").removeClass("land_phone");
        $(".responsive").addClass("land_tab");
    }
    if (browserWidth <= 736)
    {
        alert("lol");
        $(".responsive").removeClass("port_phone");
        $(".responsive").removeClass("port_tab");
        $(".responsive").removeClass("land_tab");
        $(".responsive").removeClass("land_phone");
        $(".responsive").addClass("land_phone");
    }
    if (browserWidth <= 414)
    {
        $(".responsive").removeClass("port_phone");
        $(".responsive").removeClass("port_tab");
        $(".responsive").removeClass("land_tab");
        $(".responsive").removeClass("land_phone");
        $(".responsive").addClass("port_phone");
    }
    if (browserWidth == 768)
    {
        alert("lol");
        $(".responsive").removeClass("port_phone");
        $(".responsive").removeClass("port_tab");
        $(".responsive").removeClass("land_tab");
        $(".responsive").removeClass("land_phone");
        $(".responsive").addClass("port_tab");
    }
}

$(document).ready(function() {
    dynamicLayout();
    $(window).resize(function(){
        dynamicLayout();
    });
});