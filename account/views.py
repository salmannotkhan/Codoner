from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserForm
from .models import Details
from main.models import Competition, Question, TestCase


def login_view(request):
    form = AuthenticationForm(request.POST or None)
    error = None
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
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'login.html', context=context)


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
    context = {
        'form': form,
        'competitions': competitions
    }
    return render(request, 'register.html', context=context)


@login_required(login_url='/user/login')
def dashboard_view(request):
    competitions = Competition.objects.filter(creator=request.user)

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        if title != '' and description != '':
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
        if title != '' and description != '':
            question = Question(
                title=title, description=description, competition=competition)
            question.save()
    questions = Question.objects.filter(competition=competition)
    context = {
        'competition': competition,
        'questions': questions
    }
    return render(request, 'competition.html', context=context)


@login_required(login_url='/user/login')
def question_view(request, id):
    question = Question.objects.filter(id=id).first()
    if question.competition.creator != request.user:
        return redirect('/user/')
    if request.method == 'POST':
        input = request.POST.get('input')
        output = request.POST.get('output')
        testcase = TestCase(input=input, output=output, question=question)
        testcase.save()
    testcases = TestCase.objects.filter(question=question)
    context = {
        'question': question,
        'testcases': testcases
    }
    return render(request, 'question.html', context=context)


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
    context = {
        'competitions': competitions
    }
    return render(request, 'add_question.html', context=context)
