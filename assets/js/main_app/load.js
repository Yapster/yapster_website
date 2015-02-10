function get_current_user_details() {
    // Set background cover
    // Append in section id='main_view_section' > id='column1'
    $.ajax({
        data : {
        },
        url : "/app/get_current_user_details/1/",
        type : "POST",
        success: function(newData){
            $('#column1_main').html(newData);
            $('#current_cover_image').attr('src', $('#current_user_cover_path').val());
        }
    });
}

function get_preview_libraries() {
    $.ajax({
        data : {
        },
        url : "/app/get_preview_libraries/1/",
        type : "POST",
        success: function(newData){
            $('#subscribed_libraries').html(newData);
        }
    });
}

//function get_subscribed_libraries() {
//    // Append in id=sub_section
//    $.ajax({
//        data : {
//        },
//        url : "/app/get_subscribed_libraries/1/",
//        type : "POST",
//        success: function(newData){
//            $('#subscribed_libraries').html(newData);
//        }
//    });
//}

function get_subscribed_users() {
    $.ajax({
        data : {
        },
        url : "/app/get_subscribed_users/1/",
        type : "POST",
        success: function(newData){
            $('#subscribed_users').html(newData);
        }
    });
}

function get_explore_libraries() {
    // Append in id=explore_section
    $.ajax({
        data : {
        },
        url : "//",
        type : "POST",
        success: function(newData){
            $('#explore_section').html(newData);
        }
    });
}

function get_user_details(id, pk) {
    //set background cover
    // Append in section id='user_view_section' > id='column1_user'

    var root_user = $('#' + id);
    var root_destination = $('#current_user_profile_picture');

    $('#user_cover_image').attr('src', root_user.find('.user_cover_path').val());
    root_destination.find('.gradient_profile_title').text(root_user.find('.gradient_title').text());

    var origin_pix = root_user.find('.profile_pix_center');
    $('#user_profile_picture_pix').attr('src', origin_pix.attr('src'));
    $(".prof_pix_heroable[hero-id='profile-pix-hero']").attr("hero-id", "");
    root_user.attr('hero-id', 'profile-pix-hero');

    var p = document.querySelector('#main_layer');
    var q = document.querySelector('#cover_layer');
    var r = document.querySelector('#explore_user_libraries');
    p.selected = '1';
    q.selected = '1';
    r.selected = '0';

    var url = "/app/get_user_details/" + pk + "/"
    $.ajax({
        data : {
        },
        url : url,
        type : "POST",
        success: function(newData){
            $('#details_user_profile_picture').html(newData);
        },
        error: function(newData) {
            alert('fail');
        }
    });
}

function get_user_libraries(pk) {
    // Append in id=libraries_user
    var s = document.createElement('paper-spinner');
    $('#libraries_user').html(s);

    $.ajax({
        data : {
        },
        url : "/app/get_user_libraries/" + pk + "/1/5/",
        type : "POST",
        success: function(newData){
            $('#libraries_user').html(newData);
        }
    });
}

function get_library_details(id, pk) {
    // Append in id=yaps_user
    var s = document.createElement('paper-spinner');
    $('#content_yap_library').html(s);

    var root_library = $('#' + id);
    var root_destination = $('#cover_library');

    root_destination.find('.gradient_lib_cover_title').text(root_library.find('.library_title').text());
    if (root_library.find('.library_text'))
    {
        root_destination.find('.library_description_text').text(root_library.find('.library_text').text());
    }
    else {
        root_destination.find('.library_description_text').text(root_library.find('.library_description').text());
    }

    var origin_pix = root_library.find('.library_image');
    $('#current_library_cover').attr('src', origin_pix.attr('src'));
    $(".lib_pix_heroable[hero-id='lib-pix-hero']").attr("hero-id", "");
    origin_pix.attr('hero-id', 'lib-pix-hero');
    var p = document.querySelector('#explore_user_libraries');
    p.selected = '1';

    $.ajax({
        data : {
        },
        url : "/app/get_library_details/" + pk + "/1/5/",
        type : "POST",
        success: function(newData){
            $('#content_yap_library').html(newData);
        }
    });
}

function get_playlist() {
    // Append in
    $.ajax({
        data : {
        },
        url : "//",
        type : "POST",
        success: function(newData){
            $('#cover_content').html(newData);
        }
    });
}