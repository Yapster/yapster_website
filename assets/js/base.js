$(document).ready(function() {
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
});