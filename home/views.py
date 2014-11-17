from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from home.models import Opinion, Term, Privacy, Article
from home.scripts import *


def home(request):
    return render(request, "home.html", {})

def main(request):
    """
    Home page light website
    """
    return render(request, "light_home.html", {"opinions": Opinion.objects.all(), "title_page": "Yapster"})


@csrf_exempt
def about(request):
    path = ""
    if request.POST:
        if 'send_mail' in request.POST:
            log = send_user_message(request.POST['subject'], request.POST['email'], request.POST['message'])
            return HttpResponse(log)
        if request.POST['page_content'] == "tour":
            return render(request, "about/sections/tour.html", {"title_page": "Yapster"})
        if request.POST['page_content'] == "company":
            return render(request, "about/sections/company.html", {"title_page": "Yapster"})
        if request.POST['page_content'] == "contact":
            return render(request, "about/sections/contacts.html", {"title_page": "Yapster"})
        if request.POST['page_content'] == "privacy":
            return render(request, "about/sections/privacy.html", {"privacies": Privacy.objects.all(), "title_page": "Yapster"})
        if request.POST['page_content'] == "terms":
            return render(request, "about/sections/terms.html", {"terms": Term.objects.all(), "title_page": "Yapster"})
        if 'type_page' in request.POST:
            path = request.POST['type_page']
    return render(request, "about/main_about.html", {"path": path,
                                                     "privacies": Privacy.objects.all(),
                                                     "terms": Term.objects.all(), "title_page": "Yapster | About"})


def press(request):
    articles = Article.objects.all().order_by('-id')
    return render(request, "press/main_press.html", {"articles": articles[:2], "title_page": "Yapster | Press"})
