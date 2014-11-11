function setNavBar() {
    var path = window.location.pathname;
    $(".text_menu_header").each(function(){
        if (path == $(this).attr('href'))
        {
            $(this).addClass('current');
        }
    });
}

function navigation(nameLink) {
    $.ajax({
        data : {
            type_page: nameLink,
            page_content: ""
        },
        url : "/about/",
        type : "POST",
        success: function(newData){
            $("body").html(newData);
        }
    });
}

$(document).ready(function() {
    setNavBar();
    $(".about_menu_link").click(function(){
        $('.about_menu_link').removeClass('current_page');
        $(this).addClass('current_page');
        $.ajax({
            data : {
                page_content: $(this).text()
            },
            url : "/about/",
            type : "POST",
            success: function(newData){
                if (newData) {
                    $('#about_sub_content').html(newData);
                }
            }
        });
    });
    $(".about_link").click(function() {
        navigation($(this).text());
    });
});