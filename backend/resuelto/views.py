from django.shortcuts import render, redirect
from .forms import RegistrationForm, ResolutionForm
from django.contrib.auth import authenticate, login, logout
from datetime import date
from .models import resolute
from django.views.generic.list import ListView

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


class DashboardView(ListView):
    model = resolute
    paginate_by = 5
    template_name = "dashboard.html"

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user.id)
    
    def get_context_data(self, **kwargs):
        kwargs['form'] = ResolutionForm()
        return super().get_context_data(**kwargs)

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('LoginPage')
        return super().get(request)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('LoginPage')
        form = ResolutionForm(request.POST)
        if form.is_valid():
            respost = form.save(commit=False)
            today = date.today()
            respost.done = False
            respost.author = request.user
            respost.created = today.strftime("%Y-%m-%d")
            respost.modified = today.strftime("%Y-%m-%d")
            respost.save()
        return self.get(request)

def resolutionPosts(request):
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
            #messages.success(request, you)
            return redirect('dashboard')
    #messages.error(request, "Sorry, something went wrong. Please check the provided credentials")
    return render(request, "login.html", context)


def logoutUser(request):
    logout(request)
    return redirect('LoginPage')
