from django.shortcuts import render, redirect
from .forms import RegistrationForm, ResolutionForm
from django.contrib.auth import authenticate, login, logout
from datetime import date
from .models import resolute, Joined
from django.contrib import messages


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
        print(request.POST.get('delete'))
        if request.POST.get('delete'):
            print(request.POST.get("id"))
            obj = resolute.objects.get(pk=request.POST.get("id")).delete()
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
        listz = resolute.objects.filter(author=request.user)
        return render(request, "dashboard.html", {"form": form, "list": listz})


def resolutionPosts(request):
    if request.method == "POST":
        obj = Joined()
        obj.resolution = resolute.objects.get(pk=request.POST.get("id"))
        obj.user = request.user
        obj.save()
        print("Resolution joined")
        return redirect('dashboard')

    list = resolute.objects.all()
    return render(request, "resolutionPosts.html", {"list": list})


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
            list = resolute.objects.filter(author=request.user)
            return render(request, "calendar.html", {"form": form, "list": list})
        else:
            return redirect('calendar')
    else:
        form = ResolutionForm()
        list = resolute.objects.filter(author=request.user)
        return render(request, "calendar.html", {"form": form, "list": list})


def loginPage(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            me = request.user.username
            you = f"Welcome {me}, You're succesfully logged in!"
            messages.success(request, you)
            return redirect('dashboard')
        else:
            messages.error(
                request, "Sorry, something went wrong. Please check the provided credentials")
            return render(request, "login.html", context)
    else:
        return render(request, "login.html", context)


def logoutUser(request):
    logout(request)
    return redirect('LoginPage')
