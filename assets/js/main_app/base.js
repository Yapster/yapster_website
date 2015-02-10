function uploadFile()
{
    $('#fileupload').fileupload({
        dataType: 'json',
        add: function (e, data) {
            data.context = $('<button/>').text('Upload')
                .appendTo(document.body)
                .click(function () {
                    data.context = $('<p/>').text('Uploading...').replaceAll($(this));
                    data.submit();
                });
        },
        done: function (e, data) {
            data.context.text('Upload finished.');
        }
    });
}

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
        $('#fileupload').fileupload({
            dataType: 'json',
            done: function (e, data) {
                $.each(data.result.files, function (index, file) {
                    $('<p/>').text(file.name).appendTo(document.body);
                });
            },
            progressall: function (e, data) {
                var progress = parseInt(data.loaded / data.total * 100, 10);
                $('#progress .bar').css(
                    'width',
                    progress + '%'
                );
            },
            add: function (e, data) {
                data.context = $('<button/>').text('Upload')
                    .appendTo(document.body)
                    .click(function () {
                        data.context = $('<p/>').text('Uploading...').replaceAll($(this));
                        data.submit();
                    });
            }
        });
    }
);

function toggle_core_animated(id)
{
    var p = document.querySelector('#' +  id);
    p.selected = p.selected ? 0 : 1;
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
    toggle_cover();

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
}




jQuery(document).ready(function() {
    // Loader
    get_current_user_details();
    get_preview_libraries();
    get_subscribed_users();

    // Player
    $("#player").hover(
        function () {
            var p = document.querySelector('#collapse_player');
            p.opened = 1;
        }, function () {
            var p = document.querySelector('#collapse_player');
            p.opened = 0;
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


    // initialization - first element in playlist
    //initAudio($('.current_playlist_user div:first-child'));



});