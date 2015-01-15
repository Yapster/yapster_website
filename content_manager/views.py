from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from content_manager.tools import *
from django.contrib.auth import authenticate, login, logout
from content_manager.models import *
from pydub import AudioSegment
import requests


@csrf_exempt
def log_in(request):
    """
    Display login page. Redirect to homepage if success
    TODO: Check if user is active or not
    :param request:
    :return:
    """
    logout(request)
    errors = []
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user:
                login(request, user)
                response = HttpResponseRedirect('/manager/')
                return response
        else:
            errors.append("Wrong username or password")
            return render(request, "samples/errors.html", {"errors": errors}, status=404)
    return render(request, "content_manager/login.html", {})


def forgot_password(request):
    return render(request, "content_manager/forgot_password.html", {})


def main(request):
    """
    If
    :param request:
    :return:
    """
    if request.is_ajax():
        return
    else:
        return render(request, "content_manager/landing.html", {"librairies": Library.objects.all()})


def library(request):
    """
    Manage library by adding, deleting, updating songs
    :param request:
    :return:
    """

    return render(request, "content_manager/library.html", {})


@csrf_exempt
def post_upload(request):
    if not request.FILES:
        return render(request, "No files attached", {})
    file = request.FILES[u'files[]']
    if not is_valid(file):
        return render(request, "File not valid", {})
    #error = upload_file_to_s3(file.read(), "", "1")

    return render(request, "<div>Test</div>", {})