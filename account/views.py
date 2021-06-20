from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from main.models import Question, TestCase


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
    if request.method == "POST":
        question_title = request.POST.get('question_title')
        question_desc = request.POST.get('question_desc')

        test1_input = request.POST.get('test1_input')
        test1_output = request.POST.get('test1_output')
        test2_input = request.POST.get('test2_input')
        test2_output = request.POST.get('test2_output')
        test3_input = request.POST.get('test3_input')
        test3_output = request.POST.get('test3_output')

        question = Question(title=question_title, description=question_desc)
        question.save()

        testcase = TestCase(input=test1_input,
                            output=test1_output, question=question)
        testcase.save()
        testcase = TestCase(input=test2_input,
                            output=test2_output, question=question)
        testcase.save()
        testcase = TestCase(input=test3_input,
                            output=test3_output, question=question)
        testcase.save()

    return render(request, 'add_question.html')
