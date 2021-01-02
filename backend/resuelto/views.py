from django.shortcuts import render, redirect
from .forms import RegistrationForm, ResolutionForm, ResolutionGetForm
from django.contrib.auth import authenticate, login, logout
from datetime import date
from .models import resolute

def home(request):
    form = ResolutionForm()
    return render(request, "home.html", {"form": form})


def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, "registration/signup.html", context)


def dashboard(request):
    if request.method == 'POST':
        print(request.POST)
        form = ResolutionForm(request.POST)
        if form.is_valid():
            respost = form.save(commit=False)
            today = date.today()
            respost.done = False
            respost.author = request.user
            respost.created = today.strftime("%Y-%m-%d")
            respost.modified = today.strftime("%Y-%m-%d")
            respost.save()
            form = ResolutionForm()
            return render(request, "dashboard.html", {"form": form})
        else:
            return redirect('dashboard')
    else:
        form = ResolutionForm()
        return render(request, "dashboard.html", {"form": form})


def resolutionPosts(request, **kwargs):
    resolutions = resolute.manager.get_resolutions()
        
    form = ResolutionGetForm(request.GET)
    form.is_valid()
    resolutions = resolute.manager.filter_resolutions(**form.cleaned_data)

    return render(request, "resolutionPosts.html", {"list": resolutions})


def calendar(request):
    if request.method == 'POST':
        print(request.POST)
        form = ResolutionForm(request.POST)
        if form.is_valid():
            respost = form.save(commit=False)
            today = date.today()
            respost.done = False
            respost.author = request.user
            respost.created = today.strftime("%Y-%m-%d")
            respost.modified = today.strftime("%Y-%m-%d")
            respost.save()
            form = ResolutionForm()
            return render(request, "calendar.html", {"form": form})
        else:
            return redirect('calendar')
    else:
        form = ResolutionForm()
        return render(request, "calendar.html", {"form": form})


def loginPage(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, "login.html", context)


def logoutUser(request):
    logout(request)
    return redirect('LoginPage')
