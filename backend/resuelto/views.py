from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
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
            return redirect('home')
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, "registration/signup.html", context)


def dashboard(request):
    return render(request, "dashboard.html", {})


def calendar(request):
    return render(request, "calendar.html", {})
