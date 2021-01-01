from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def home(request):
    return render(request, "home.html", {})


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
    return render(request, "dashboard.html", {})


def calendar(request):
    return render(request, "calendar.html", {})


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
