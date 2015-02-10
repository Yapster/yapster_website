from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from main_app.tools import *
from django.contrib.auth import authenticate, login, logout
from main_app.models import *
from pydub import AudioSegment


def forgot_password(request):
    return render(request, "main_app/other_pages/forgot_password.html", {})

def main(request):
    """
    If
    :param request:
    :return:
    """
    if request.is_ajax():
        return
    else:
        return render(request, "main_app/other_pages/landing.html", {"librairies": Library.objects.all()})

def library(request):
    """
    Manage library by adding, deleting, updating songs
    :param request:
    :return:
    """

    return render(request, "main_app/other_pages/library.html", {})

@csrf_exempt
def post_upload(request):
    if not request.FILES:
        return render(request, "No files attached", {})
    file = request.FILES[u'files[]']
    if not is_valid(file):
        return render(request, "File not valid", {})
    #error = upload_file_to_s3(file.read(), "", "1")

    return render(request, "<div>Test</div>", {})


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
        return HttpResponse(username)
    else:
        return HttpResponseNotAllowed()


@csrf_exempt
def get_current_user_details(request,
                             user_id,
                             path='http://api.yapster.co/users/load/profile/info/'):
    """
    From API get current user logged in information
    :param request:
    :param user_id: Current user id
    :return: Html + user info
    """
    context = {}

    params = {"user_id": 1,
              "session_id": 54,
              "profile_user_id": 2}
    json_response = yapster_api_post_request(path, params).json()
    if json_response['valid']:
        data = json_response['data']
        context['first_name'] = data['first_name']
        context['last_name'] = data['last_name']
        context['id'] = data['id']
        context['city'] = data['city_name']
        context['country'] = data['country_name']
        context['profile_picture_pix'] = get_profile_pix_path(data['profile_picture_path'])
        context['description'] = data['description']
        context['web_cover_picture_1_path'] = get_profile_pix_path(data['web_cover_picture_1_path'])

    return render(request, "main_app/sub_templates/current_user_details.html", context)


@csrf_exempt
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

    params = {"user_id": 1,
              "session_id": 54}

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

    params = {"user_id": 1,
              "session_id": 54,
              "profile_user_id": 2}
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

    params = {"user_id": 1,
              "session_id": 54,
              "profile_user_id": 2}
    json_response = yapster_api_post_request(path, params).json()
    if json_response['valid']:
        data = json_response['data']
        context['user_0_profile_pix'] = get_profile_pix_path(data[0]['profile_picture_path'])
        context['user_0_first_name'] = data[0]['first_name']
        context['user_0_last_name'] = data[0]['last_name']
        context['user_0_id'] = data[0]['id']
        context['user_0_web_cover_picture_1_path'] = get_profile_pix_path(data[0]['web_cover_picture_1_path'])

        context['user_1_profile_pix'] = get_profile_pix_path(data[1]['profile_picture_path'])
        context['user_1_first_name'] = data[1]['first_name']
        context['user_1_last_name'] = data[1]['last_name']
        context['user_1_id'] = data[1]['id']
        context['user_1_web_cover_picture_1_path'] = get_profile_pix_path(data[1]['web_cover_picture_1_path'])

        context['user_2_profile_pix'] = get_profile_pix_path(data[2]['profile_picture_path'])
        context['user_2_first_name'] = data[2]['first_name']
        context['user_2_last_name'] = data[2]['last_name']
        context['user_2_id'] = data[2]['id']
        context['user_2_web_cover_picture_1_path'] = get_profile_pix_path(data[2]['web_cover_picture_1_path'])

    return render(request, "main_app/sub_templates/subscribed_users.html", context)


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

    params = {"user_id": 1,
              "session_id": 54,
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
def get_user_libraries(request,
                       user_id,
                       page,
                       amount,
                       path="http://api.yapster.co/users/load/profile/libraries/"):
    """
    From API get user libraries from clicked user
    :param request:
    :param user_id: Clicked user id
    :return: Html with list of user libraries + libs pix
    """
    context = {}

    params = {"user_id": 1,
              "session_id": 54,
              "profile_user_id": int(user_id),
              "page": int(page),
              "amount": int(amount)
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

    return render(request, "main_app/sub_templates/user_libraries.html", context)


@csrf_exempt
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

    params = {"user_id": 1,
              "session_id": 54,
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
                 library_id,
                 yap_id,
                 page,
                 amount,
                 path="http://api.yapster.co/yap/load/library/yaps/"):
    """
    From API get the playlist of the
    :param request:
    :param library_id:
    :param yap_id:
    :return:
    """

    context = {}

    params = {"user_id": 1,
              "session_id": 54,
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
            d['name'] = sub_data['user']['first_name'] + sub_data['user']['last_name']
            d['current'] = d['id'] == int(yap_id)
            l_yaps.append(d)
        context['l_yaps'] = l_yaps
        context['number_yaps'] = len(data)
        context['library_id'] = library_id

    return render(request, "main_app/sub_templates/get_playlist.html", context)
