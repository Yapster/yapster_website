from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from home.models import Opinion, Term, Privacy

def home(request):
    return render(request, "home.html", {})

def main(request):
    """
    Home page light website
    """
    return render(request, "light_home.html", {"opinions": Opinion.objects.all()})


@csrf_exempt
def about(request):
    if request.POST:
        if request.POST['page_content'] == "tour":
            return render(request, "about/sections/terms.html", {"terms": Term.objects.all()})
        if request.POST['page_content'] == "company":
            return render(request, "about/sections/company.html", {})
        if request.POST['page_content'] == "contact":
            return render(request, "about/sections/contacts.html", {})
        if request.POST['page_content'] == "privacy":
            return render(request, "about/sections/privacy.html", {"privacies": Privacy.objects.all()})
        if request.POST['page_content'] == "terms":
            return render(request, "about/sections/terms.html", {"terms": Term.objects.all()})

    return render(request, "about/main_about.html", {})