function get_current_user_details() {
    // Set background cover
    // Append in section id='main_view_section' > id='column1'
    $('#current_cover_image').html("<paper-spinner active></paper-spinner>");

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
    $('#subscribed_libraries_results').html("<paper-spinner active></paper-spinner>");


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

function get_subscribed_users() {
    $('#subscribed_users_results').html("<paper-spinner active></paper-spinner>");

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

function get_user_details(id, pk) {
    //set background cover
    // Append in section id='user_view_section' > id='column1_user'
    $('#details_user_profile_picture').html("<paper-spinner active></paper-spinner>");

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
    $('#results_all_view').html("<paper-spinner active></paper-spinner>");


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
    $('#content_yap_library').html("<paper-spinner active></paper-spinner>");

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
    $('#current_library_cover').attr('src', origin_pix.attr('src'));
    $(".lib_pix_heroable[hero-id='lib-pix-hero']").attr("hero-id", "");
    origin_pix.attr('hero-id', 'lib-pix-hero');
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

function get_view_all_users(id, pk)
{
    $('#results_all_view').html("");
    $('#results_all_view').addClass('sub_users');
    $('#results_all_view').removeClass('sub_libraries');
    $('#results_all_view').html("<template-library id='fake_template'></template-library>");

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
    $('#results_all_view').append("<template-library id='fake_template'></template-library>");
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
    $('#results_all_view').append("<template-library id='fake_template'></template-library>");


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
    var url = "app/get_all_libraries/"
    $('#results_all_view').append("<template-library id='fake_template'></template-library>");


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

function get_search_results()
{

}

function get_explore_users()
{
    $('#explore_users_results').html("<paper-spinner active></paper-spinner>");

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
    $('#explore_libraries_results').html("<paper-spinner active></paper-spinner>");

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