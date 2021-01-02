from django.shortcuts import render
from .forms import ResolutionForm
# Create your views here.


def home(request):
    form = ResolutionForm()
    return render(request, "home.html", {"form": form})


def login(request):
    return render(request, "login.html", {})


def signup(request):
    return render(request, "signup.html", {})


def dashboard(request):
    return render(request, "dashboard.html", {})


def calendar(request):
    return render(request, "calendar.html", {})
