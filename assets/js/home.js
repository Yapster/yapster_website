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
    var nav = navigator.userAgent;
    if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(nav))
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
}


function log_in(username, password)
{
    $.ajax({
        url: 'http://jsonip.com/',
        success: function(newData){
            ip = newData.ip;
            $.ajax({
                data : {

                    username: username,
                    password: password,
                    ip: ip
                },
                url : "/app/login/",
                type : "POST",
                success: function(){
                    window.location.replace("/app/");
                },
                error: function() {
                    $('#errorlogin').html('Email/username and/or password invalid.');

                }
            });
        },
        error: function(data){
            alert('ip marche pas');
        }
    });
}

$(document).ready(function() {

    dynamicLayout();
    $(window).resize(function(){
        dynamicLayout();
    });
    $('#login_button').hover(function(){
        $('#inputs_container').show("slide", {direction: "right"}, 1000);
    });
    $('#login_button').click(function(){
        log_in($('#username').val(), $('#password').val());
    });
    $('.press_enter').keyup(function(event){
        if (event.keyCode == 13) {
            log_in($('#username').val(), $('#password').val());
        }
    });
});