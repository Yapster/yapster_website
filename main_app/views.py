from django.contrib.gis.geometry.regex import json_regex
from django.shortcuts import render, redirect
from django.http import HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twisted.conch.test.test_userauth import userauth
from main_app.tools import *
from decorators import user_has_perm
from pydub import AudioSegment
from math import trunc



def forgot_password(request):
    return render(request, "main_app/other_pages/forgot_password.html", {})

@user_has_perm
def main(request,
         path='http://api.yapster.co/users/load/profile/info/'):
    """
    If
    :param request:
    :return:
    """

    context = {}

    params = {
        "user_id": request.COOKIES['u'],
        "session_id": request.COOKIES['s'],
        "profile_user_id": request.COOKIES['u']
    }

    json_response = yapster_api_post_request(path, params).json()

    if json_response['valid']:
        # Get user info
        data = json_response['data']
        context['subscriber_users_count'] = data['subscriber_users_count']
        context['subscribing_users_count'] = data['subscribing_users_count']
        context['subscribing_libraries_count'] = data['subscribing_libraries_count']
        context['libraries_count'] = data['libraries_count']

    return render(request, "main_app/base.html", context)


def library(request):
    """
    Manage library by adding, deleting, updating songs
    :param request:
    :return:
    """

    return render(request, "main_app/other_pages/library.html", {})


@csrf_exempt
def pre_upload(request):
    """
    Create forms for each yap to upload
    :param request:
    :return: Html page with each yap, inputs
    """
    context = {}
    if request.POST:
        seconds = int(request.POST['seconds'].split('.')[0])
        filename = request.POST['filename']
        nb_parts = trunc(seconds / 60)

        context['nb_parts'] = nb_parts
        context['loop_times'] = [i+1 for i in range(nb_parts)]
        context['filename'] = filename.split('.')[0]
        context['last_time'] = seconds % 60
        return render(request, "main_app/other_pages/edit_cut_yap.html", context)
    return render(request, "main_app/other_pages/edit_cut_yap.html", context)


@csrf_exempt
@user_has_perm
def get_library_upload(request,
                       path="http://api.yapster.co/users/load/profile/libraries/"):
    """
    Get user libraries and return Html with each library available
    :param request:
    :param path: API Call Url
    :return: Html with each library
    """
    context = {}
    params = {"user_id": request.COOKIES['u'],
              "session_id": request.COOKIES['s'],
              "profile_user_id": request.COOKIES['u'],
              "page": int(request.POST['page']),
              "amount": int(request.POST['amount'])
    }

    json_response = yapster_api_post_request(path, params).json()
    if json_response['valid']:
        data = json_response['data']
        l_libs = []
        for i in range(0, len(data)):
            d_new = {}
            d_new['picture_cropped_path'] = get_profile_pix_path(data[i]['picture_cropped_path'])
            d_new['title'] = data[i]['title']
            d_new['description'] = data[i]['description']
            d_new['id'] = data[i]['id']

            l_libs.append(d_new)

        context['libraries'] = l_libs
        context['number_libraries'] = len(data)

    return render(request, "main_app/other_pages/upload_yap__libraries.html", context)


@csrf_exempt
def post_upload(request):
    if not request.FILES:
        return render(request, "No files attached", {})
    audio_file = request.FILES[u'yap_audio[]']
    if u'yap_pix[]' in request.FILES:
        pix_file = request.FILES[u'yap_pix[]']

    if not audio_is_uploaded(audio_file, request.COOKIES['u']):
        return render(request, "Audio File not valid", {})
    #error = upload_file_to_s3(file.read(), "", "1")
    if not pix_is_uploaded(pix_file, request.COOKIES['u'], ""):
        return render(request, "Image File is not valid", {})
    return render(request, "<div>Test</div>", {})


@csrf_exempt
def post_new_cover(request):
    #upload cover
    if not request.FILES:
        return render(request, "No File attached", {})
    file = request.FILES[u'files[]']
    if not is_valid_pix(file, request.COOKIES['u'], "cover"):
        return render(request, "File not valid", {})

    #save cover in profile


    return render(request, "<div></div>", {})

@csrf_exempt
def post_new_pix(request):
    #upload pix
    if not request.FILES:
        return render(request, "No File attached", {})
    file = request.FILES[u'files[]']
    if not is_valid_pix(file, request.COOKIES['u'], "profile"):
        return render(request, "File not valid", {})



    #save pix in profile
    return render(request, "<div></div>", {})


# Ajax requests Handler / API Interface

@csrf_exempt
def log_in(request,
           path='http://api.yapster.co/users/sign_in/'):
    """
    POST request only. Redirect to Dashboard if success.
    TODO: Check if user is active or not
    :param request:
    :return:
    """
    username = request.POST['username']
    pwd = request.POST['password']
    ip = request.POST['ip']

    if "@" in username:
        option_type = "email"
    else:
        option_type = "username"

    params = {
        'option': username,
        'option_type': option_type,
        'password': pwd,
        'device_type': "computer",
        'identifier': ip
    }

    json_response = yapster_api_post_request(path, params).json()

    if json_response['valid']:
        response = redirect("/app/")
        response.set_cookie('s', json_response['session_id'])
        response.set_cookie('u', json_response['user_id'])
        return response
    else:
        return HttpResponseNotAllowed()


def log_out(request):
    request
    return render(request, "home.html", {})

@csrf_exempt
@user_has_perm
def get_current_user_details(request,
                             user_id,
                             path='http://api.yapster.co/users/load/profile/info/',
                             path_countries='http://api.yapster.co/location/countries/load/',
                             path_states='http://api.yapster.co/location/us_states/load/'):
    """
    From API get current user logged in information
    :param request:
    :param user_id: Current user id
    :return: Html + user info
    """
    context = {}

    params = {
        "user_id": request.COOKIES['u'],
        "session_id": request.COOKIES['s'],
        "profile_user_id": request.COOKIES['u']
    }
    params_states = {
        "country_id": 184
    }

    json_response = yapster_api_post_request(path, params).json()
    json_response_countries = yapster_api_post_request(path_countries, {}).json()
    json_response_states = yapster_api_post_request(path_states, params_states).json()

    if json_response['valid']:
        # Get user info
        data = json_response['data']
        context['first_name'] = data['first_name']
        context['last_name'] = data['last_name']
        context['id'] = data['id']
        context['city'] = data['city_name']
        context['country'] = data['country_name']
        context['profile_picture_pix'] = get_profile_pix_path(data['profile_picture_path'])
        context['description'] = data['description']
        context['subscribing_users_count'] = data['subscribing_users_count']
        context['subscribing_libraries_count'] = data['subscribing_libraries_count']
        context['web_cover_picture_1_path'] = get_profile_pix_path(data['web_cover_picture_1_path'])

        # Get countries
        l_countries = []
        if json_response_countries:
            for country in json_response_countries:
                l_countries.append(country['name'])
            context['countries'] = l_countries

        # Get states
        l_states = []
        if json_response_states:
            for state in json_response_states:
                l_states.append(state['name'])
            context['states'] = l_states


    return render(request, "main_app/sub_templates/current_user_details.html", context)


@csrf_exempt
@user_has_perm
def get_preview_libraries(request,
                          user_id,
                          path='http://api.yapster.co/users/load/dashboard/subscribed/libraries/'):
    """
    From API get 3 libraries and 3 yaps for each from current user
    :param request:
    :param user_id: Current user id
    :return: Html + lib + yaps data
    """
    context = {}

    params = {"user_id": request.COOKIES['u'],
              "session_id": request.COOKIES['s']}

    json_response = yapster_api_post_request(path, params).json()

    if json_response['valid']:
        data = json_response['data']

        l_libraries = []
        for i in range(0, 3):
            d = {}
            d['library_profile_pix'] = get_profile_pix_path(data[i]['picture_cropped_path'])
            d['library_title'] = data[i]['title']
            d['library_id'] = data[i]['id']
            d['library_description'] = data[i]['description']

            d['web_cover_picture_1_path'] = get_profile_pix_path(data[i]['user']['web_cover_picture_1_path'])


            l_libraries.append(d)
        context['l_libraries'] = l_libraries

        l_list_of_yaps = []
        for i in range(0, 3):
            l_yaps = []
            for j in range(0, 3):
                d = {}
                d['date_created'] = data[i]['yaps'][j]['date_created']
                sub_data = data[i]['yaps'][j]['yap_info']
                d['title'] = sub_data['title']
                d['description'] = sub_data['description']
                d['id'] = sub_data['id']
                d['first_name'] = sub_data['user']['first_name']
                d['last_name'] = sub_data['user']['last_name']
                d['picture_cropped_path'] = get_profile_pix_path(sub_data['picture_cropped_path'])
                d['audio_path'] = get_profile_pix_path(sub_data['audio_path'])

                l_yaps.append(d)
            l_list_of_yaps.append(l_yaps)
        context['l_list_of_yaps'] = l_list_of_yaps


    return render(request, "main_app/sub_templates/subscribed_libraries.html", context)

@csrf_exempt
@user_has_perm
def get_subscribed_libraries(request,
                             user_id,
                             path='http://api.yapster.co/users/load/dashboard/subscribed/libraries/'):
    """
    From API get subscribed libraries from current user
    :param request:
    :param user_id: Current user id
    :return: Html + lib data
    """
    context = {}

    params = {"user_id": request.COOKIES['u'],
              "session_id": request.COOKIES['s'],
              "profile_user_id": request.COOKIES['u']}
    json_response = yapster_api_post_request(path, params).json()
    if json_response['valid']:
        data = json_response['data']

        context['library_0_profile_pix'] = get_profile_pix_path(data[0]['picture_cropped_path'])
        context['library_0_title'] = data[0]['title']
        context['library_0_id'] = data[0]['id']

        context['library_1_profile_pix'] = get_profile_pix_path(data[1]['picture_cropped_path'])
        context['library_1_title'] = data[1]['title']
        context['library_1_id'] = data[1]['id']

        context['library_2_profile_pix'] = get_profile_pix_path(data[2]['picture_cropped_path'])
        context['library_2_title'] = data[2]['title']
        context['library_2_id'] = data[2]['id']

    return render(request, "main_app/sub_templates/subscribed_libraries.html", context)


@csrf_exempt
def get_subscribed_users(request,
                         user_id,
                         path="http://api.yapster.co/users/load/dashboard/subscribed/users/"):
    """
    From API get subscribed users from current user
    :param request:
    :param user_id: Current user id
    :return: Html + users data
    """
    context = {}

    params = {"user_id": request.COOKIES['u'],
              "session_id": request.COOKIES['s'],
              "profile_user_id": request.COOKIES['u']}

    json_response = yapster_api_post_request(path, params).json()
    if json_response['valid']:
        data = json_response['data']
        context['user_0_profile_pix'] = get_profile_pix_path(data[0]['profile_picture_path'])
        context['user_0_first_name'] = data[0]['first_name']
        context['user_0_last_name'] = data[0]['last_name']
        context['user_0_id'] = data[0]['id']
        context['user_0_web_cover_picture_1_path'] = get_profile_pix_path(data[0]['web_cover_picture_1_path'])
        context['followed_0'] = data[0]['viewing_user_subscribed_to_user']

        context['user_1_profile_pix'] = get_profile_pix_path(data[1]['profile_picture_path'])
        context['user_1_first_name'] = data[1]['first_name']
        context['user_1_last_name'] = data[1]['last_name']
        context['user_1_id'] = data[1]['id']
        context['user_1_web_cover_picture_1_path'] = get_profile_pix_path(data[1]['web_cover_picture_1_path'])
        context['followed_1'] = data[1]['viewing_user_subscribed_to_user']

        context['user_2_profile_pix'] = get_profile_pix_path(data[2]['profile_picture_path'])
        context['user_2_first_name'] = data[2]['first_name']
        context['user_2_last_name'] = data[2]['last_name']
        context['user_2_id'] = data[2]['id']
        context['user_2_web_cover_picture_1_path'] = get_profile_pix_path(data[2]['web_cover_picture_1_path'])
        context['followed_2'] = data[2]['viewing_user_subscribed_to_user']

    return render(request, "main_app/sub_templates/subscribed_users.html", context)

@user_has_perm
def get_explore_libraries(request,
                          user_id):
    """
    From API get explore libraries from current user
    :param request:
    :param user_id: Current user id
    :return: Html + lib data
    """
    context = {}
    return render(request, "main_app/sub_templates/explore_libraries.html", context)


@csrf_exempt
@user_has_perm
def get_user_details(request,
                     user_id,
                     path="http://api.yapster.co/users/load/profile/info/"):
    """
    From API get user details from user id clicked.
    :param request:
    :param user_id: Clicked user id
    :return: Html with profile pix and common user info
    """
    context = {}
    params = {}

    params = {"user_id": request.COOKIES['u'],
              "session_id": request.COOKIES['s'],
              "profile_user_id": user_id}

    json_response = yapster_api_post_request(path, params).json()

    if json_response['valid']:
        data = json_response['data']

        context['first_name'] = data['first_name']
        context['last_name'] = data['last_name']
        context['description'] = data['description']
        context['country'] = data['country_name']
        context['city'] = data['city_name']
        context['id'] = data['id']
        context['city'] = data['city_name']
        context['web_cover_picture_1_path'] = data['web_cover_picture_1_path']

    return render(request, 'main_app/sub_templates/user_details.html', context)

@csrf_exempt
@user_has_perm
def get_user_libraries(request,
                       path="http://api.yapster.co/users/load/profile/libraries/"):
    """
    From API get user libraries from clicked user
    :param request:
    :param user_id: Clicked user id
    :return: Html with list of user libraries + libs pix
    """
    context = {}

    params = {"user_id": int(request.COOKIES['u']),
              "session_id": int(request.COOKIES['s']),
              "profile_user_id": int(request.POST['user_id']),
              "page": int(request.POST['page']),
              "amount": int(request.POST['amount'])
    }

    json_response = yapster_api_post_request(path, params).json()

    if json_response['valid']:
        data = json_response['data']
        l_libs = []
        for i in range(0, len(data)):
            d_new = {}
            d_new['picture_cropped_path'] = get_profile_pix_path(data[i]['picture_cropped_path'])
            d_new['title'] = data[i]['title']
            d_new['description'] = data[i]['description']
            d_new['id'] = data[i]['id']
            d_new['subscribed'] = data[i]['viewing_user_subscribed_to_library']

            l_libs.append(d_new)

        context['libraries'] = l_libs
        context['number_libraries'] = data[0]['user']['libraries_count']

    return render(request, "main_app/sub_templates/user_libraries.html", context)


@csrf_exempt
@user_has_perm
def get_library_details(request,
                        library_id,
                        page,
                        amount,
                        path='http://api.yapster.co/yap/load/library/yaps/'):
    """
    From API get library detail from clicked library
    :param request:
    :param library_id: Clicked library id
    :return:  Html with list of yap + lib pix
    """
    context = {}

    params = {"user_id": request.COOKIES['u'],
              "session_id": request.COOKIES['s'],
              "library_id": int(library_id),
              "page": int(page),
              "amount": int(amount)
    }

    json_response = yapster_api_post_request(path, params).json()

    if json_response['valid']:
        data = json_response['data']
        l_yaps = []
        for i in range(0, len(data)):
            d = {}
            d['date_created'] = data[i]['date_created']
            sub_data = data[i]['yap_info']
            d['title'] = sub_data['title']
            d['description'] = sub_data['description']
            d['audio_path'] = get_profile_pix_path(sub_data['audio_path'])
            d['picture_cropped_path'] = get_profile_pix_path(sub_data['picture_cropped_path'])
            d['id'] = sub_data['id']
            d['first_name'] = sub_data['user']['first_name']
            d['last_name'] = sub_data['user']['last_name']
            l_yaps.append(d)
        context['l_yaps'] = l_yaps
        context['number_yaps'] = len(data)
        context['library_id'] = library_id
    return render(request, "main_app/sub_templates/library_details.html", context)


@csrf_exempt
def get_playlist(request,
                 path="http://api.yapster.co/yap/load/library/yaps/"):
    """
    From API get the playlist of the
    :param request:
    :param library_id:
    :param yap_id:
    :return:
    """

    context = {}
    library_id = request.POST['library_id']
    yap_id = int(request.POST['yap_id'])
    params = {"user_id": request.COOKIES['u'],
              "session_id": request.COOKIES['s'],
              "library_id": int(library_id),
              "page": 1,
              "amount": 100
    }

    json_response = yapster_api_post_request(path, params).json()

    if json_response['valid']:
        data = json_response['data']
        l_yaps = []
        for i in range(0, len(data)):
            d = {}
            d['date_created'] = data[i]['date_created']
            sub_data = data[i]['yap_info']
            d['title'] = sub_data['title']
            d['description'] = sub_data['description']
            d['audio_path'] = get_profile_pix_path(sub_data['audio_path'])
            # d['picture_cropped_path'] = get_profile_pix_path(sub_data['picture_cropped_path'])
            d['id'] = sub_data['id']
            d['name'] = sub_data['user']['first_name'] + sub_data['user']['last_name']
            d['current'] = d['id'] == yap_id
            l_yaps.append(d)
        context['l_yaps'] = l_yaps
        context['number_yaps'] = len(data)
        context['library_id'] = library_id
        # context['library_name'] =

    return render(request, "main_app/sub_templates/get_playlist.html", context)

@csrf_exempt
def get_all_users(request,
                  path="http://api.yapster.co/users/load/dashboard/subscribed/users/"):


    context = {}
    d = request.POST
    params = {"user_id": request.COOKIES['u'],
              "session_id": request.COOKIES['s'],
              "page": d['page'],
              "amount": d['amount']
    }

    json_response = yapster_api_post_request(path, params).json()

    if json_response['valid']:
        data = json_response['data']
        l_users = []
        for i in range(0, len(data)):
            d = {}
            sub_data = data[i]
            d['first_name'] = sub_data['first_name']
            d['last_name'] = sub_data['last_name']
            d['id'] = sub_data['id']
            d['profile_picture_path'] = get_profile_pix_path(sub_data['profile_picture_path'])
            d['description'] = sub_data['description']
            d['city_name'] = sub_data['city_name']
            l_users.append(d)

        context['l_users'] = l_users

    return render(request, "main_app/sub_templates/all_users_subscribed.html", context)


@csrf_exempt
@user_has_perm
def get_all_libraries(request,
                      path="http://api.yapster.co/users/load/dashboard/subscribed/libraries/"):


    context = {}
    d = request.POST
    params = {"user_id": request.COOKIES['u'],
              "session_id": request.COOKIES['s'],
              "page": d['page'],
              "amount": d['amount']
    }

    json_response = yapster_api_post_request(path, params).json()

    if json_response['valid']:
        data = json_response['data']
        l_libraries = []
        for i in range(0, len(data)):
            d = {}
            sub_data = data[i]
            d['title'] = sub_data['title']
            d['description'] = sub_data['description']
            d['id'] = sub_data['id']
            d['picture_cropped_path'] = get_profile_pix_path(sub_data['picture_cropped_path'])
            d['web_cover_picture_1_path'] = get_profile_pix_path(sub_data['user']['web_cover_picture_1_path'])
            l_libraries.append(d)

        context['l_libraries'] = l_libraries

    return render(request, "main_app/sub_templates/all_libraries_subscribed.html", context)


@csrf_exempt
@user_has_perm
def get_search_results(request,
                       path="http://api.yapster.co/search/default/"):

    context = {}
    d = request.POST
    params = {
        "user_id": request.COOKIES['u'],
        "session_id": request.COOKIES['s'],
        "text": d['search'],
        "screen": "web",
        "search_type": "all"
    }

    json_response = yapster_api_post_request(path, params).json()
    if json_response['valid']:
        data = json_response['data']

        #Users Handling
        l_users = data['users']
        try:
            l_users[0]
            context['user_0_profile_pix'] = get_profile_pix_path(l_users[0]['profile_picture_path'])
            context['user_0_first_name'] = l_users[0]['first_name']
            context['user_0_last_name'] = l_users[0]['last_name']
            context['user_0_id'] = l_users[0]['id']
            context['user_0_web_cover_picture_1_path'] = get_profile_pix_path(l_users[0]['web_cover_picture_1_path'])
            context['followed_0'] = l_users[0]['viewing_user_subscribed_to_user']
        except IndexError:
            pass
        try:
            l_users[1]
            context['user_1_profile_pix'] = get_profile_pix_path(l_users[1]['profile_picture_path'])
            context['user_1_first_name'] = l_users[1]['first_name']
            context['user_1_last_name'] = l_users[1]['last_name']
            context['user_1_id'] = l_users[1]['id']
            context['user_1_web_cover_picture_1_path'] = get_profile_pix_path(l_users[1]['web_cover_picture_1_path'])
            context['followed_1'] = l_users[1]['viewing_user_subscribed_to_user']
        except IndexError:
            pass
        try:
            l_users[2]
            context['user_2_profile_pix'] = get_profile_pix_path(l_users[2]['profile_picture_path'])
            context['user_2_first_name'] = l_users[2]['first_name']
            context['user_2_last_name'] = l_users[2]['last_name']
            context['user_2_id'] = l_users[2]['id']
            context['user_2_web_cover_picture_1_path'] = get_profile_pix_path(l_users[2]['web_cover_picture_1_path'])
            context['followed_2'] = l_users[2]['viewing_user_subscribed_to_user']
        except IndexError:
            pass

        #Libraries Handling
        data_libs = data['libraries']
        l_libs = []
        for i in range(0, len(data)):
            d_new = {}
            d_new['picture_cropped_path'] = get_profile_pix_path(data_libs[i]['picture_cropped_path'])
            d_new['title'] = data_libs[i]['title']
            d_new['description'] = data_libs[i]['description']
            d_new['id'] = data_libs[i]['id']

            l_libs.append(d_new)

        context['libraries'] = l_libs
        context['number_libraries'] = len(data)

        #Yap Handling

        data_yaps = data['yaps']
        l_yaps = []
        for i in range(0, len(data_yaps)):
            d = {}
            sub_data = data_yaps[i]
            d['title'] = sub_data['title']
            d['description'] = sub_data['description']
            d['audio_path'] = get_profile_pix_path(sub_data['audio_path'])
            d['picture_cropped_path'] = get_profile_pix_path(sub_data['picture_cropped_path'])
            d['id'] = sub_data['id']
            d['first_name'] = sub_data['user']['first_name']
            d['last_name'] = sub_data['user']['last_name']
            l_yaps.append(d)
        context['l_yaps'] = l_yaps


    return render(request, "main_app/other_pages/search_templates/search_results.html", context)

@csrf_exempt
@user_has_perm
def get_explore_users(request,
                      path="http://api.yapster.co/users/load/dashboard/subscribed/users/"):
    context = {}
    d = request.POST
    params = {
        "user_id": request.COOKIES['u'],
        "session_id": request.COOKIES['s'],
        "profile_user_id": request.COOKIES['u']
    }
    json_response = yapster_api_post_request(path, params).json()
    # if json_response['valid']:
    #     data = json_response['data']
    #     context['user_0_profile_pix'] = get_profile_pix_path(data[0]['profile_picture_path'])
    #     context['user_0_first_name'] = data[0]['first_name']
    #     context['user_0_last_name'] = data[0]['last_name']
    #     context['user_0_id'] = data[0]['id']
    #     context['user_0_web_cover_picture_1_path'] = get_profile_pix_path(data[0]['web_cover_picture_1_path'])
    #
    #     context['user_1_profile_pix'] = get_profile_pix_path(data[1]['profile_picture_path'])
    #     context['user_1_first_name'] = data[1]['first_name']
    #     context['user_1_last_name'] = data[1]['last_name']
    #     context['user_1_id'] = data[1]['id']
    #     context['user_1_web_cover_picture_1_path'] = get_profile_pix_path(data[1]['web_cover_picture_1_path'])
    #
    #     context['user_2_profile_pix'] = get_profile_pix_path(data[2]['profile_picture_path'])
    #     context['user_2_first_name'] = data[2]['first_name']
    #     context['user_2_last_name'] = data[2]['last_name']
    #     context['user_2_id'] = data[2]['id']
    #     context['user_2_web_cover_picture_1_path'] = get_profile_pix_path(data[2]['web_cover_picture_1_path'])



    return render(request, "main_app/sub_templates/all_users_explore.html", context)

@csrf_exempt
@user_has_perm
def get_explore_libraries(request,
                          path="http://api.yapster.co/users/load/dashboard/subscribed/libraries/"):
    context = {}
    d = request.POST
    params = {
        "user_id": request.COOKIES['u'],
        "session_id": request.COOKIES['s'],
        "profile_user_id": request.COOKIES['u']
    }
    json_response = yapster_api_post_request(path, params).json()
    # if json_response['valid']:
    #     data = json_response['data']
    #     l_libraries = []
    #     for i in range(0, len(data)):
    #         d = {}
    #         sub_data = data[i]
    #         d['title'] = sub_data['title']
    #         d['description'] = sub_data['description']
    #         d['id'] = sub_data['id']
    #         d['picture_cropped_path'] = get_profile_pix_path(sub_data['picture_cropped_path'])
    #         d['web_cover_picture_1_path'] = get_profile_pix_path(sub_data['user']['web_cover_picture_1_path'])
    #         l_libraries.append(d)
    #
    #     context['l_libraries'] = l_libraries


    return render(request, "main_app/sub_templates/all_libraries_explore.html", context)



@csrf_exempt
@user_has_perm
def edit_current_user_profile(request,
                              path="http://api.yapster.co/users/settings/edit/"):
    context = {}
    params = {
        "user_id": request.COOKIES['u'],
        "session_id": request.COOKIES['s'],
        }

    json_response = yapster_api_post_request(path, params).json()

    #if json_response['valid']:


    return render(request, "", context)


@csrf_exempt
@user_has_perm
def subscribed_user_profile(request,
                            path="http://api.yapster.co/yap/subscribe/user/"):
    context = {}
    params = {
        "user_id": request.COOKIES['u'],
        "session_id": request.COOKIES['s'],
        "user_2_id": request.POST['to_follow']
    }

    json_response = yapster_api_post_request(path, params).json()
    if json_response['valid']:
        return HttpResponse()
    return HttpResponseNotAllowed()

@csrf_exempt
@user_has_perm
def unsubscribed_user_profile(request,
                              path="http://api.yapster.co/yap/unsubscribe/user/"):
    context = {}
    params = {
        "user_id": request.COOKIES['u'],
        "session_id": request.COOKIES['s'],
        "user_2_id": request.POST['to_unfollow']
    }

    json_response = yapster_api_post_request(path, params).json()
    if json_response['valid']:
        return HttpResponse()
    return HttpResponseNotAllowed()


@csrf_exempt
@user_has_perm
def subscribe_library(request,
                      path="http://api.yapster.co/yap/subscribe/library/"):
    context = {}

    params = {
        "user_id": request.COOKIES['u'],
        "session_id": request.COOKIES['s'],
        "library_id": request.POST['library_to_follow']
    }

    json_response = yapster_api_post_request(path, params).json()
    if json_response['valid']:
        return HttpResponse()

    return HttpResponseNotAllowed()


@csrf_exempt
@user_has_perm
def unsubscribe_library(request,
                        path="http://api.yapster.co/yap/unsubscribe/library/"):
    context = {}

    params = {
        "user_id": request.COOKIES['u'],
        "session_id": request.COOKIES['s'],
        "library_id": request.POST['library_to_unfollow']
    }

    json_response = yapster_api_post_request(path, params).json()
    if json_response['valid']:
        return HttpResponse()
    return HttpResponseNotAllowed()