function get_current_user_details()
{
    // Set background cover
    // Append in section id='main_view_section' > id='column1'
    $('#current_cover_image').html("<loading-data id=fake_template class='loading_data' datatype='profile'></loading-data>");


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

function get_preview_libraries()
{
    $('#subscribed_libraries_results').html("<loading-data id=fake_template class='loading_data' datatype='libraries1'></loading-data>");


    $.ajax({
        data : {
        },
        url : "/app/get_preview_libraries/1/",
        type : "POST",
        success: function(newData){
            $('#subscribed_libraries_results').html(newData);
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

function get_subscribed_users()
{
    $('#subscribed_users_results').html("<loading-data id=fake_template class='loading_data' datatype='users'></loading-data>");

    $.ajax({
        data : {
        },
        url : "/app/get_subscribed_users/1/",
        type : "POST",
        success: function(newData){
            $('#subscribed_users_results').html(newData);
        }
    });
}

function get_user_details(id, pk)
{
    //set background cover
    // Append in section id='user_view_section' > id='column1_user'
    $('#details_user_profile_picture').html("<loading-data id=fake_template class='loading_data' datatype='profile'></loading-data>");

    var root_user = $('#' + id);
    var root_destination = $('#current_user_profile_picture');

    $('#user_cover_image').attr('src', root_user.find('.user_cover_path').val());
    root_destination.find('.gradient_profile_title').text(root_user.find('.user_title').text());

    var origin_pix = root_user.find('.profile_pix_tag');
    $('#user_profile_picture_pix').attr('src', origin_pix.attr('src'));
    $(".prof_pix_heroable[hero-id='profile-pix-hero']").attr("hero-id", "");
    root_user.attr('hero-id', 'profile-pix-hero');




    var bool_follow = root_user.find('.user_followed').val();
    if (bool_follow == "True")
    {
        $('#follow_profile').attr('icon', 'done').addClass("followed");
    }
    else
    {
        $('#follow_profile').attr('icon', 'add');
    }

    var p = document.querySelector('#main_layer');
    var q = document.querySelector('#cover_layer');
    var r = document.querySelector('#explore_user_libraries');

    p.selected = '1';
    q.selected = '1';
    r.selected = '0';

    var url = "/app/get_user_details/" + pk + "/";
    $.ajax({
        data : {
        },
        url : url,
        type : "POST",
        success: function(newData){
            $('#details_user_profile_picture').html(newData);
        },
        error: function(newData) {
        }
    });
}

function get_user_libraries(pk)
{
    // Append in id=libraries_user
    $('#libraries_user').html("<loading-data id=fake_template class='loading_data' datatype='libraries3'></loading-data>");

    $.ajax({
        data : {
            user_id: pk,
            page: 1,
            amount: 20
        },
        url : "/app/get_user_libraries/",
        type : "POST",
        success: function(newData){
            $('#libraries_user').html(newData);
        }
    });
}

function get_library_details(id, pk)
{
    // Append in id=yaps_user
    $('#content_yap_library').html("<loading-data id=fake_template class='loading_data' datatype='yaps'></loading-data>");

    var root_library = $('#' + id);
    var root_destination = $('#cover_library');

    $('#user_cover_image').attr('src', root_library.find('.user_cover_path').val());
    root_destination.find('.gradient_lib_cover_title').text(root_library.find('.library_title').text());
    if (root_library.find('.library_text'))
    {
        root_destination.find('.library_description_text').text(root_library.find('.library_text').text());
    }
    else {
        root_destination.find('.library_description_text').text(root_library.find('.library_description').text());
    }

    var origin_pix = root_library.find('.library_image');
    root_destination.find(".library_description_button").attr("library_id", root_library.find('.id').val());
    root_destination.find(".library_description_button").attr("followed", root_library.find('.subscribed').val());

    $('#current_library_cover').attr('src', origin_pix.attr('src'));
    $(".lib_pix_heroable[hero-id='lib-pix-hero']").attr("hero-id", "");
    origin_pix.attr('hero-id', 'lib-pix-hero');

    $(".prof_pix_heroable[hero-id='profile-pix-hero']").attr("hero-id", "");


    $('#user_profile_picture_pix').attr('src', root_library.find('.profile_picture_path').val());

    var p = document.querySelector('#explore_user_libraries');
    var q = document.querySelector('#cover_layer');
    var r = document.querySelector('#main_layer');

    p.selected = '1';
    q.selected = '1';
    r.selected = '1';

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

function set_user_details(id, pk)
{
    var root_library = $('#' + id);
    var root_destination = $('#current_user_profile_picture');

    root_destination.find(".gradient_profile_title").text(root_library.find(".name").val());
    root_destination.find(".gradient_details").text(root_library.find(".location").val());
    $("#details_user_profile_picture").text(root_library.find(".user_description").val());
    $("#user_profile_picture_pix").attr('src', root_library.find(".profile_picture_path").val());
    if (root_library.find(".profile_cover"))
    {
        $("#user_cover_image").attr('src', root_library.find(".profile_cover").val());
    }

}


function get_view_all_users(id, pk)
{
    $('#results_all_view').html("");
    $('#results_all_view').addClass('sub_users');
    $('#results_all_view').removeClass('sub_libraries');
    $('#results_all_view').html("<loading-data id=fake_template class='loading_data' datatype='users'></loading-data>");

    $('#button_back_view_all_to_main').show();
    var url = "app/get_all_users/";


    $('#view_all_title').text('Subscribed Users');
    $('#view_all_dashboard').find('.number_header_title').text('Users');
    $('#view_all_dashboard').find('.number_header_number').text('21');


    $.ajax({
        data : {
            page: 1,
            amount: 10
        },
        url : url,
        type : "POST",
        success: function(newData){
            $('#fake_template').remove();
            $('#results_all_view').html(newData);
            in_load = false;
        },
        error: function(newData) {

        }
    });
}

function get_view_all_users_more(id, pk, page)
{
    $('#results_all_view').append("<loading-data id=fake_template class='loading_data loading_more' datatype='users'></loading-data>");
    var url = "app/get_all_users/"

    $.ajax({
        data : {
            user_id: 1,
            session_id: 54,
            page: page,
            amount: 10
        },
        url : url,
        type : "POST",
        success: function(newData){
            $('#fake_template').remove();
            $('#results_all_view').append(newData);
            in_load = false;
        },
        error: function(newData) {
            $('#fake_template').remove();
            $('#results_all_view').append("<no-more-to-load typeData='users'></no-more-to-load>");
        }
    });
}

function get_view_all_libraries(id, pk)
{
    $('#results_all_view').html("");
    $('#results_all_view').addClass('sub_libraries');
    $('#results_all_view').removeClass('sub_users');

    var url = "app/get_all_libraries/";
    $('#results_all_view').append("<loading-data id=fake_template class='loading_data' datatype='libraries4'></loading-data>");


    $('#view_all_title').text('Subscribed Libraries');
    $('#view_all_dashboard').find('.number_header_title').text('Libraries');
    $('#view_all_dashboard').find('.number_header_number').text('21');


    $.ajax({
        data : {
            page: 1,
            amount: 10
        },
        url : url,
        type : "POST",
        success: function(newData){
            $('#fake_template').remove();
            $('#results_all_view').html(newData);
            $('#results_all_view').addClass('sub_libraries');

            in_load = false;
        },
        error: function(newData) {
            $('#fake_template').remove()
        }
    });
}

function get_view_all_libraries_more(id, pk, page)
{
    var url = "app/get_all_libraries/";
    $('#results_all_view').append("<loading-data id=fake_template class='loading_data loading_more' datatype='libraries5'></loading-data>");


    $.ajax({
        data : {
            user_id: 1,
            session_id: 54,
            page: page,
            amount: 10
        },
        url : url,
        type : "POST",
        success: function(newData){
            $('#fake_template').remove();
            $('#results_all_view').append(newData);
            in_load = false;
        },
        error: function(newData) {
            $('#fake_template').remove();
        }
    });
}

function get_explore_users()
{
    $('#explore_users_results').html("<loading-data id=fake_template class='loading_data' datatype='users'></loading-data>");

    $.ajax({
        data : {
        },
        url : "/app/get_explore_users/",
        type : "POST",
        success: function(newData){
            $('#explore_users_results').html(newData);
        }
    });
}

function get_explore_libraries()
{
    $('#explore_libraries_results').html("<loading-data id=fake_template class='loading_data' datatype='libraries6'></loading-data>");

    $.ajax({
        data : {
        },
        url : "/app/get_explore_libraries/",
        type : "POST",
        success: function(newData){
            $('#explore_libraries_results').html(newData);
        }
    });
}


function specific_search(type_search)
{
    $('#specific_search_results_content').html("<loading-data id=fake_template class='loading_data' datatype='search results'></loading-data>");

    $.ajax({
        data : {
            type: type_search,
            page: 1,
            amount: 5
        },
        url : "/app/get_all_search_results/",
        type : "POST",
        success: function(newData){
            $('#specific_search_results_content').html(newData);
        }
    });
}

function specific_search_more(type_search, page)
{
    $('#specific_search_results_content').append("<loading-data id=fake_template class='loading_data' datatype='users'></loading-data>");

}