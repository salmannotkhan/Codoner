from unittest import result
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserForm
from .models import Detail
from main.models import Competition, Question, Result, TestCase


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
        id = request.POST.get('competition', False)
        if form.is_valid() and id:
            user = form.save()
            competition = Competition.objects.filter(id=id).first()
            detail = Detail(
                id=user, competition=competition)
            detail.save()
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
        input = request.POST.get('input', False)
        output = request.POST.get('output', False)
        if input and output:
            testcase = TestCase(input=input, output=output, question=question)
            testcase.save()
    testcases = TestCase.objects.filter(question=question)
    context = {
        'question': question,
        'testcases': testcases
    }
    return render(request, 'question.html', context=context)


def result_view(request, id):
    competition = Competition.objects.filter(id=id).first()
    users = User.objects.filter(detail__competition=competition)
    questions = Question.objects.filter(competition=competition)
    results = Result.objects.filter(
        user__in=users, question__in=questions)
    user_results = []
    for user in users:
        user_result = {}
        user_result['user'] = user
        question_list = []
        for question in questions:
            r = {}
            r['question'] = question
            result = results.filter(user=user, question=question).first()
            if result:
                r['testcases'] = [bool(i) for i in result.testcase.split(',')]
            question_list.append(r)
        user_result['questions'] = question_list
        user_results.append(user_result)

    print(user_results)

    context = {
        'competition': competition,
        'user_results': user_results
    }
    return render(request, 'result.html', context=context)
