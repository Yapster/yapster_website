var in_load = true;
var cpt_users_call = 1;
var cpt_libraries_call = 1;
var preview_audio;

function log_in()
{
    $.ajax({
        type : "POST",
        data : {
            username: $("#username").val(),
            password: $("#password").val()
        },
        url : "/manager/login/",
        error: function(newData) {
            $("#errors").html(newData);
        },
        complete: function(status, text){
            $("#errors").html(text);
        },
        success: function() {
            window.location.replace("http://127.0.0.1:8000/manager/");
        }
    });
}

$(function ()
    {
        $( "#new_yap_upload" ).change(function(e) {
            var file = e.currentTarget.files[0];
            filename = file.name;

            objectUrl = URL.createObjectURL(file);
            $('#new_yap_upload_audio').prop("src", objectUrl);
        });

        $("#new_yap_upload_audio").on("canplaythrough", function(e){
            var seconds = e.currentTarget.duration;
            $.ajax({
                data : {
                    seconds: seconds,
                    filename: filename
                },
                url : "/app/post/pre_upload/",
                type : "POST",
                success: function(newData){
                    $('.editing_part').html(newData);
//                    preview_audio = new Audio(objectUrl);
                    $.ajax({
                        data : {
                            page: 1,
                            amount: 5
                        },
                        url : "/app/post/get_library_upload/",
                        type : "POST",
                        success: function(newData){
                            $('.edit_yap_libraries').html(newData);
                        }
                    });
                }
            });
            URL.revokeObjectURL(objectUrl);
        });

        $("#new_yap_photo_upload").change(function(e) {
            var file = e.currentTarget.files[0];

            var pixUrl = URL.createObjectURL(file);
            $('.new_yap_photo_upload_pix').prop("src", pixUrl);
        });

        $(".filename_aftercut_text").click(function(){
            var part = this.attr('part');
            preview_audio.currentTime = part * 60;
            preview_audio.play();
        });

    }
);


function choose_library(id)
{
    $(".edit_yap_library").removeClass("select");
    $("#" + id).addClass("select");
}

function post_yap()
{
    // Get filenames
    // Get photo file
    // Get library picked
    // get audio file



    $.ajax({
        data : {
            seconds: seconds,
            filename: filename
        },
        url : "/app/post/pre_upload/",
        type : "POST",
        success: function(newData){
            $('.editing_part').html(newData);
//                    preview_audio = new Audio(objectUrl);
            $.ajax({
                data : {
                    page: 1,
                    amount: 5
                },
                url : "/app/post/get_library_upload/",
                type : "POST",
                success: function(newData){
                    $('.edit_yap_libraries').html(newData);
                }
            });
        }
    });
}

$(function ()
    {
        $('#post_yap_button').fileupload({
            dataType: 'json',
            done: function (e, data) {
                $.each(data.result.files, function (index, file) {
                    $('<p/>').text(file.name).appendTo(document.body);
                });
            },
            add: function (e, data) {
                data.submit();
            }
        });
    }
);


function toggle_core_animated(id)
{
    var p = document.querySelector('#' +  id);
    p.selected = p.selected ? 0 : 1;
}

function toggle_yap_edit()
{
    $('#edit-yap').toggleClass('on');
}

function stuff(x)
{
    var p = document.querySelector('#main_layer');
    p.selected = x;
}

function toggle_left_column(id)
{
    var p = document.querySelector('#' + id);
    p.selected = p.selected ? 0 : 1;
    $('.interface_hideable_items').toggleClass('hide');
}

function save_edit_current_user(id)
{
    toggle_left_column(id);
}

function follow_user()
{
    var state = $('#follow_profile').attr('icon');
    var user_id = $('#id_user_detail').val();


    if (state == 'add-circle')
    {
        $.ajax({
            data : {
                to_follow: user_id
            },
            url : "/app/subscribed_user_profile/",
            type : "POST",
            success: function(){
                $('#follow_profile').attr('icon', 'remove-circle');
            }
        });
    }
    else
    {
        $.ajax({
            data : {
                to_unfollow: user_id
            },
            url : "/app/unsubscribed_user_profile/",
            type : "POST",
            success: function(){
                $('#follow_profile').attr('icon', 'add-circle');
            }
        });
    }
}


function to_main_to_user(id, pk)
{
    get_user_details(id, pk);
    get_user_libraries(pk);
}

function to_main_to_library(id, pk)
{
    get_library_details(id, pk);

    var p = document.querySelector('#main_layer');
    p.selected = '1';
}

function to_user_to_library(id, pk)
{
    get_library_details(id, pk);

}

function to_library_to_user()
{
    var p = document.querySelector('#explore_user_libraries');
    p.selected = '0';
}

function user_to_main(x)
{
    var p = document.querySelector('#main_layer');
    var q = document.querySelector('#cover_layer');
    p.selected = x;
    q.selected = x;
}

function test(x)
{
    var p = document.querySelector('#center_layer');
    p.selected = x;
}

function tog_right()
{
    var p = document.querySelector('#right_side');
    p.selected = p.selected ? 0 : 1;
}

function from_dashboard_to_view_all_user()
{
    var current_title = $('#view_all_title').text();

    $("#view_all_libraries_container").attr("hero-id", "");
    $("#view_all_users_container").attr("hero-id", "view_all_hero");

    var p = document.querySelector('#view_all_layer');
    p.selected = 1;

    $('#button_from_view_all_to_dash').toggle();


    if (current_title != "Subscribed Users")
    {
        cpt_users_call = 1;
        get_view_all_users(1, 54);
    }

}

function from_dashboard_to_view_all_library()
{
    var current_title = $('#view_all_title').text();

    $("#view_all_users_container").attr("hero-id", "");
    $("#view_all_libraries_container").attr("hero-id", "view_all_hero");

    var p = document.querySelector('#view_all_layer');
    p.selected = 1;

    $('#button_from_view_all_to_dash').toggle();


    if (current_title != "Subscribed Libraries")
    {
        cpt_libraries_call = 1;
        get_view_all_libraries(1, 54);
    }

}

function from_view_all_to_dashboard()
{
    $('#button_from_view_all_to_dash').toggle();
    var p = document.querySelector('#view_all_layer');
    p.selected = 0;
}

function tog_dialog()
{
    var p = document.querySelector('#cover_preview_card');
    if (p.selected == 2) {
        p.selected = 0;
    }
    else
    {
        p.selected = p.selected ? 0 : 1;
    }
}

function instanciate_button()
{
    var dom = document.createElement('preview-yap');
    $("#cover_content").append(dom);
}

function toggle_details(id)
{
    var p = document.querySelector('#' + id);
    p.opened = p.opened ? 0 : 1;
}

function toggle_perso_interface()
{
    $('#column3').toggleClass('tall_cover');
    $('#column2').toggleClass('tall_cover');
    $('.current_playlist_user').toggleClass('current_playlist_user_on');
    $('.search_results').toggle();
}

function change_profile_pix(input)
{
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#my_profile_picture_pix')
                .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}


jQuery(document).ready(function() {
    // Loader
    get_current_user_details();
    get_preview_libraries();
    get_subscribed_users();
    get_explore_users();
    get_explore_libraries();

    // Player
    $("#player").hover(
        function () {
            var p = document.querySelector('#collapse_player');
            p.opened = 1;
            $('#current_yap_pix').fadeIn(800);

        }, function () {
            var p = document.querySelector('#collapse_player');
            p.opened = 0;
            $('#current_yap_pix').fadeOut(800);
        }
    );

    $('#left_part').click(
        function () {

        }
    );

// play click
    $('#play_button').click(function (e) {
        e.preventDefault();

        playAudio();
    });

// pause click
    $('#pause_button').click(function (e) {
        e.preventDefault();
        stopAudio();
    });

// forward click
    $('.fwd').click(function (e) {
        e.preventDefault();

        stopAudio();

        var next = $('.current_playlist_user div.active').next();
        if (next.length == 0) {
            next = $('.current_playlist_user div:first-child');
        }
        initAudio(next);
    });

// rewind click
    $('.rew').click(function (e) {
        e.preventDefault();

        stopAudio();

        var prev = $('.current_playlist_user div.active').prev();
        if (prev.length == 0) {
            prev = $('.current_playlist_user div:last-child');
        }
        initAudio(prev);
    });

// show playlist
    $('.pl').click(function (e) {
        e.preventDefault();

        $('.current_playlist_user').fadeIn(300);
    });

    document.querySelector('#core-header-view_all').addEventListener('scroll', function(e){
        if ((e.detail.target.scrollHeight -  e.detail.target.scrollTop) == e.detail.target.offsetHeight){
            if (!in_load)
            {
                in_load = true;
                var current_title = $('#view_all_title').text();
                if (current_title == "Subscribed Users")
                {
                    cpt_users_call++;
                    get_view_all_users_more(1,4,cpt_users_call);
                }
                else {
                    cpt_libraries_call++;
                    get_view_all_libraries_more(1, 4, cpt_libraries_call);
                }

            }
        }
    });
});