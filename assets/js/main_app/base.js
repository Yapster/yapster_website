var in_load = true;
var cpt_users_call = 1;
var cpt_libraries_call = 1;
var preview_audio;
var previous_profile_pix;
var previous_cover_pix;

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

// Events Upload new yap
$(function ()
    {
        var filesList = [],
            paramNames = [],
            array_filename = {},
            elem = $("#file_upload_yap_post");
        file_upload = elem.fileupload({
            formData: array_filename,
            autoUpload: false,
            fileInput: $("input:file")
        }).on("fileuploadadd", function(e, data){
            filesList.push(data.files[0]);
            paramNames.push(e.delegatedEvent.target.name);
        });

        $("#post_yap_button").click(function(e){
            e.preventDefault();

            file_upload.fileupload('send', {files:filesList, paramName: paramNames, formData: new_array});
        });

        $("#new_yap_upload").change(function(e) {
            var file = e.currentTarget.files[0];
            filename = file.name;

            objectUrl = URL.createObjectURL(file);
            $('#new_yap_upload_audio').prop("src", objectUrl);
        });

//        $("#file_upload_yap_post").fileupload({
//            url: '/app/post/upload/',
//            add: function (e, data) {
//                alert('class file_upload');
//                $("#post_yap_button").unbind("click");
//                $('#post_yap_button').click(function(){
//                    alert('event_in');
//                    data.submit();
//                });
//            }
//        });

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

// Functions upload Yap
function choose_library(id)
{
    $(".edit_yap_library").removeClass("select");
    $("#" + id).addClass("select");
    var title_lib = $("#" + id).find(".edit_yap_library_title_container").text();
    $(".text_library_selected").text("Selected library: " + title_lib);
    new_array['library'] = id;
}

$(function ()
    {
        $('#post_yap_button').fileupload({
            dataType: 'json',
            done: function (e, data) {
                alert(data.result);
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


// Cover events
$(function ()
{
    $('#current_user_cover').hover(
        function () {
            $('#cover_button').removeClass('hide');

        }, function () {
            $('#cover_button').addClass('hide');
        }
    );

    $("#new_cover_upload").change(function(e) {

        previous_cover_pix = $("#current_cover_image").attr("src");
        var file = e.currentTarget.files[0];

        var pixUrl = URL.createObjectURL(file);
        $('#current_cover_image').prop("src", pixUrl);
    });

    $('#new_cover_upload').fileupload({
        dataType: 'json',
        add: function (e, data) {
            toggle_cover_button();
            $('#button_valid_cover').click(function(){
                data.submit();
                $(".cover_button").removeClass("show_cover_button");
            });
        }
    });
});

// Cover functions
function toggle_cover_button()
{
    $(".cover_button").addClass("show_cover_button");
}

function cancel_cover()
{
    $('#current_cover_image').prop("src", previous_cover_pix);
    previous_cover_pix = "";
    $(".cover_button").removeClass("show_cover_button");
}

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


function save_edit_current_user(id)
{
    toggle_left_column(id);
}



function follow_user()
{
    var state = $('#follow_profile').attr('icon');
    var user_id = $('#id_user_detail').val();


    if (state == 'add')
    {
        $.ajax({
            data : {
                to_follow: user_id
            },
            url : "/app/subscribed_user_profile/",
            type : "POST",
            success: function(){
                $('#follow_profile').attr('icon', 'done').addClass("followed");
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
                $('#follow_profile').attr('icon', 'add').removeClass("followed");
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
    set_user_details(id, pk);
    var p = document.querySelector('#main_layer');
    p.selected = '1';
}


function to_user_to_library(id, pk)
{
    $("#button_back_library_to_user").attr('onclick', "to_library_to_user()");
    get_library_details(id, pk);
}

function to_search_to_library(id, pk)
{
    $("#button_back_library_to_user").attr('onclick', "to_library_to_user()");
    get_library_details(id, pk);
    set_user_details(id, pk);
}

function to_library_to_user()
{
    $("#button_back_library_to_user").attr('onclick', "user_to_main()");
    var p = document.querySelector('#explore_user_libraries');
    p.selected = '0';
}

function user_to_main()
{
    var p = document.querySelector('#main_layer');
    var q = document.querySelector('#cover_layer');
    p.selected = '0';
    q.selected = '0';
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

function from_general_search_to_specific_search(id_clicked)
{
    alert(id_clicked);
    $(".view_all_search_container").attr("hero-id", "");
    $("#" + id_clicked).attr("hero-id", "specific_search_results");

    specific_search(id_clicked);
    var p = document.querySelector("#search_results_animation");
    p.selected = 1;

}

function from_specific_search_to_general_search(){
    var p = document.querySelector("#search_results_animation");
    p.selected = 0;
}

function from_dashboard_to_view_all_user()
{
    var current_title = $('#view_all_title').text();

    $("#view_all_libraries_container").attr("hero-id", "");
    $("#view_all_users_container").attr("hero-id", "view_all_hero");

    var p = document.querySelector('#view_all_layer');
    p.selected = 1;

    $('#button_back_view_all_to_main').show();


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

    $('#button_back_view_all_to_main').show();


    if (current_title != "Subscribed Libraries")
    {
        cpt_libraries_call = 1;
        get_view_all_libraries(1, 54);
    }

}

function from_view_all_to_dashboard()
{
    $('#button_back_view_all_to_main').hide();
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

function toggle_playlist()
{
    $('#column3').toggleClass('tall_cover');
    $('#column2').toggleClass('tall_cover');
    $('.current_playlist_user').toggleClass('current_playlist_user_on');
    $('.search_results').fadeToggle();
}


// Functions change profile pix
function change_profile_pix(input)
{
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        previous_profile_pix = $("#my_profile_picture_pix").attr('src');
        reader.onload = function (e) {
            $('#my_profile_picture_pix')
                .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function toggle_left_column(id)
{
    var p = document.querySelector('#' + id);
    p.selected = p.selected ? 0 : 1;
    $('.interface_hideable_items').toggleClass('hide');
    $("#done_edit_user_button").unbind("click");
}

$(function ()
{

});

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

        var next = $('.current_playlist_user div.selected_yap').next();
        if (next.length == 0) {
            next = $('.current_playlist_user div:first-child');
        }
        initAudio(next);
    });

// rewind click
    $('.rew').click(function (e) {
        e.preventDefault();

        stopAudio();

        var prev = $('.current_playlist_user div.selected_yap').prev();
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

    $("#follow_profile").hover(function(){
        $(".followed").attr("icon", "close");
    }, function(){
        $(".followed").attr("icon", "done");
    });
});

document.querySelector('paper-slider').addEventListener('change', function(event){
    console.log(event.target.value);
    song.currentTime = event.target.value;
});