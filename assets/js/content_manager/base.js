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

$(function () {
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
});

function stuff(x) {
    var p = document.querySelector('#main_layer');
    p.selected = x;
}

function to_main_to_user(id, x)
{
    $(".prof_pix_heroable[hero-id='profile-pix-hero']").attr("hero-id", "");
    $('#' + id).attr('hero-id', 'profile-pix-hero');
    var p = document.querySelector('#main_layer');
    p.selected = x;
}

function user_to_main(x) {
    var p = document.querySelector('#main_layer');
    p.selected = x;
}

function test(x) {
    var p = document.querySelector('#center_layer');
    p.selected = x;
}

function tog_right() {
    var p = document.querySelector('#right_side');
    p.selected = p.selected ? 0 : 1;
}

function tog_dialog() {
    var p = document.querySelector('#cover_preview_card');
    if (p.selected == 2) {
        p.selected = 0;
    }
    else
    {
        p.selected = p.selected ? 0 : 1;
    }
}

function instanciate_button() {
    var dom = document.createElement('task-list');
    $("#cover_content").append(dom);
}