from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import UserForm
from .models import Details
from main.models import Competition, Question, TestCase


def login_view(request):
    form = AuthenticationForm(request.POST or None)
    error = None
    print(form.fields)
    if request.method == 'POST':
        user = authenticate(
            username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user=user)
            if user.is_staff:
                return redirect(request.GET.get('next', '/user'))
            else:
                return redirect(request.GET.get('next', '/code'))
        error = 'Invalid username/password'
    return render(request, 'login.html', context={'form': form, 'error': error})


def logout_view(request):
    logout(request)
    return redirect('/user/login')


def signup_view(request):
    form = UserForm()
    competitions = Competition.objects.all()
    if request.method == 'POST':
        form = UserForm(request.POST)
        competition_name = request.POST.get('competition', False)
        if form.is_valid() and competition_name:
            user = form.save()
            details = Details(
                id=user, competition_name=request.POST.get('competition'))
            details.save()
            return redirect('/user/login/')
    return render(request, 'register.html', context={'form': form, 'competitions': competitions})


@login_required(login_url='/user/login')
def dashboard_view(request):
    competitions = Competition.objects.filter(creator=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title is not '' and description is not '':
            competition = Competition(
                title=title, description=description, creator=request.user)
            competition.save()
    return render(request, 'dashboard.html', context={'competitions': competitions})


@login_required(login_url='/user/login')
def competition_view(request, id):
    competition = Competition.objects.filter(id=id).first()
    if request.user != competition.creator:
        return redirect('/user/')
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title is not '' and description is not '':
            competition = Competition(
                title=title, description=description, creator=request.user)
            competition.save()
    return render(request, 'competition.html', context={'competition': competition})


def add_view(request):
    competitions = Competition.objects.filter(creator=request.user)
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

    return render(request, 'add_question.html', context={'competitions': competitions})
