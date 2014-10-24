from django.shortcuts import render
from home.models import Opinion

def home(request):
    return render(request, "home.html", {})

def main(request):
    """
    Home page light website
    """
    return render(request, "main.html", {"opinions": Opinion.objects.all()})