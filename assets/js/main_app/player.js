var song;
var slider = $('.tracker');

function event_change_slider()
{

}

function initAudio(elem) {
    var url = elem.attr('audiourl');
    var title = elem.find('.yap_in_playlist_title').text();
    var cover = elem.attr('cover');
    var artist = elem.attr('artist');

    if (song)
    {
        stopAudio();
    }

    $('.yap_in_playlist').removeClass('selected_yap');
    elem.addClass('selected_yap');

    $('#details_player_title').text(title);
    $('#details_player_detail').text(artist);
    $('#current_yap_pix').attr('src', cover);

    song = new Audio(url);



    // timeupdate event listener
    song.addEventListener('timeupdate',function (){
        var curtime = parseInt(song.currentTime, 10);
        var minutes = Math.floor(curtime / 60);
        var seconds = Math.floor(curtime % 60);
        if (seconds < 10)
        {
            seconds = "0" + seconds;
        }

        $('.tracker').attr('value', curtime);
        $('#start_time').text(minutes + ":" + seconds);
    });

    song.addEventListener('loadedmetadata', function(){
        $('.tracker').attr('max', parseInt(song.duration));
        var time = parseInt(song.duration, 10);
        var minutes = Math.floor(time / 60);
        var seconds = Math.floor(time % 60);

        if (seconds < 10)
        {
            seconds = "0" + seconds;
        }

        $('#end_time').text(minutes + ":" + seconds);
    });

    song.addEventListener('ended', function(e){
        e.preventDefault();
        stopAudio();
        var next = $('.current_playlist_user div.selected_yap').next();
        if (next.length == 0) {
            next = $('.current_playlist_user div:first-child');
        }
        initAudio(next);
    });



//    $('.current_playlist_user div').removeClass('selected_yap');

    song.play();

    $('#play_button').addClass('hide_icon');
    $('#pause_button').removeClass('hide_icon');
}
function playAudio() {
    song.play();

    $('#play_button').addClass('hide_icon');
    $('#pause_button').removeClass('hide_icon');
}
function stopAudio() {
    song.pause();

    $('#play_button').removeClass('hide_icon');
    $('#pause_button').addClass('hide_icon');
}

function set_playlist(title, library_id, yap_image_in_lib, url, author, yap_id, library_title) {

    $('#details_player_title').text(title);
    $('#details_player_detail').text(author);
    $('#current_yap_pix').attr('src', yap_image_in_lib);
    if (library_id) {
        var text_header = author + " - " + library_title;
        $(".playlist_header_text").text(text_header);
    }

    if (song)
    {
        stopAudio();
    }

    song = new Audio(url);

    song.addEventListener('timeupdate',function (){
        var curtime = parseInt(song.currentTime, 10);
        var minutes = Math.floor(curtime / 60);
        var seconds = Math.floor(curtime % 60);
        if (seconds < 10)
        {
            seconds = "0" + seconds;
        }

        $('.tracker').attr('value', curtime);
        $('#start_time').text(minutes + ":" + seconds);
    });

    song.addEventListener('loadedmetadata', function(){
        $('.tracker').attr('max', parseInt(song.duration));
        var time = parseInt(song.duration, 10);
        var minutes = Math.floor(time / 60);
        var seconds = Math.floor(time % 60);

        if (seconds < 10)
        {
            seconds = "0" + seconds;
        }

        $('#end_time').text(minutes + ":" + seconds);
    });

    song.addEventListener('ended', function(e){
        e.preventDefault();
        stopAudio();
        var next = $('.current_playlist_user div.selected_yap').next();
        if (next.length == 0) {
            next = $('.current_playlist_user div:first-child');
        }
        initAudio(next);
    });


    song.play();
    $('#play_button').addClass('hide_icon');
    $('#pause_button').removeClass('hide_icon');

    $('.playlist_container').html("<loading-data class='loading_data' datatype='yaps'></loading-data>");

    $.ajax({
        data : {
            library_id: library_id,
            yap_id: yap_id
        },
        url : "/app/get_playlist/",
        type : "POST",
        success: function(newData){
            $('.playlist_container').html(newData);
        },
        error: function(){
            $('.playlist_container').html("");
        }
    });
}


function play_yap(yap){
    set_playlist($("#" + yap ).find(".yap_title").text(),
        $("#" + yap).find(".library_id").val(),
        $("#" + yap).find(".yap_image_in_lib").attr('src'),
        $("#" + yap).find(".yap_path").val(),
        $("#" + yap).find(".author").val(),
        $("#" + yap).find(".yap_id").val(),
        $(".gradient_lib_cover_title").text()
    )
};

function play_library_yap(yap, library_id, library_title){
    set_playlist($("#" + yap ).find(".library_yap_title").text(),
        library_id,
        $("#" + yap).find(".library_yap_image").attr('src'),
        $("#" + yap).find(".yap_path").val(),
        $("#" + yap).find(".author").val(),
        $("#" + yap).find(".yap_id").val(),
        library_title
    )
};

function play_yap_in_playlist(yap_in_playlist_id) {
    initAudio($("#" + yap_in_playlist_id));
}