from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def login_view(request):
    form = AuthenticationForm(request.POST or None)
    error = None
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user=user)
            if user.is_staff:
                return redirect('/user/')
            else:
                return redirect('/code/playground')
        error = 'Username or password incorrect'
    return render(request, 'login.html', context={'form': form, 'error': error})


def logout_view(request):
    logout(request)
    return redirect('/code/playground')


def signup_view(request):
    form = UserCreationForm(request.POST or None)
    error = None
    return render(request, 'register.html', context={'form': form, 'error': error})


def dashboard_view(request):
    return render(request, 'dashboard.html')


def add_view(request):
    return render(request, 'add_question.html')
