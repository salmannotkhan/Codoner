import os
import subprocess
from django.http import JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Question, Result, TestCase


@login_required(login_url='/user/login/')
def index(request):
    questions = Question.objects.filter(
        competition=request.user.detail.competition)
    context = {
        'questions': questions
    }
    return render(request, 'index.html', context=context)


@login_required(login_url='/user/login/')
def playground(request, id):
    question = get_object_or_404(Question, id=id)
    testcases = TestCase.objects.filter(question=question)
    if request.method == 'POST':
        lang = request.POST['language']
        filename = request.user.username + '.' + lang
        code = request.POST.get('code')
        open(filename, 'w').write(code)
        testcase_results = []
        for testcase in range(len(testcases)):
            if lang == 'py':
                result = python_execute(question.id, testcase, filename)
            elif lang == 'c':
                result = c_execute(question.id, testcase, filename)
            elif lang == 'java':
                result = java_execute(question.id, testcase, filename)
            testcase_results.append(str(int(result['passed'])))
        os.remove(filename)
        result = Result(user=request.user, question=question,
                        testcase=','.join(testcase_results), lang=lang, code=code)
        result.save()
        return redirect('/code')
    context = {
        'question': question,
        'testcase': testcases[0],
        'totalTestCases': len(testcases)
    }
    return render(request, 'playground.html', context=context)


def c_execute(question_id: int, test_id: int, filename: str):
    question = Question.objects.filter(id=question_id).first()
    testcase = TestCase.objects.filter(question=question)[test_id]
    output_file = filename.replace('.c', '.out')
    comp = subprocess.run(['gcc', filename, '-o', output_file],
                          stderr=subprocess.PIPE, text=True)
    if comp.stderr:
        result = {
            'passed': False,
            'error': comp.stderr
        }
        return result
    result = {'passed': True}
    code = subprocess.Popen(['./' + output_file], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        output, error = code.communicate(input=testcase.input, timeout=2)
        output = '\r\n'.join(output.splitlines(keepends=False))
        if output != testcase.output:
            result['passed'] = False
            if error:
                result['error'] = error
            else:
                result['error'] = output
    except subprocess.TimeoutExpired:
        result['passed'] = False
        result['error'] = 'Code execution timed out'
    os.remove(output_file)
    return result


def java_execute(question_id: int, test_id: int, filename: str):
    # TODO: Fix Class thingy. Not usable right now.
    code_snippet = f'public class {filename.replace(".java", "")} {{{open(filename, "r").read()}}}'
    open(filename, 'w').write(code_snippet)
    output_file = filename.replace('.java', '')
    question = Question.objects.filter(id=question_id).first()
    testcase = TestCase.objects.filter(question=question)[test_id]
    comp = subprocess.run(['javac', filename],
                          stderr=subprocess.PIPE, text=True)
    if comp.stderr:
        result = {
            'passed': False,
            'error': comp.stderr
        }
        return result
    result = {'passed': True}
    code = subprocess.Popen(['java',  output_file], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    try:
        output, error = code.communicate(
            input=testcase.input, timeout=2)
        output = '\r\n'.join(output.splitlines(keepends=False))
        if output != testcase.output:
            result['passed'] = False
            if error:
                result['error'] = error
            else:
                result['error'] = output
    except subprocess.TimeoutExpired:
        result['passed'] = False
        result['error'] = 'Code execution timed out'
    os.remove(output_file + '.class')
    return result


def python_execute(question_id: int, test_id: int, filename: str):
    question = Question.objects.filter(id=question_id).first()
    testcase = TestCase.objects.filter(question=question)[test_id]
    code = subprocess.Popen(['python3', filename], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    result = {'passed': True}
    try:
        output, error = code.communicate(input=testcase.input, timeout=2)
        output = '\r\n'.join(output.splitlines(keepends=False))
        if output != testcase.output:
            result['passed'] = False
            if error:
                result['error'] = error
            else:
                result['error'] = output
    except subprocess.TimeoutExpired:
        result['passed'] = False
        result['error'] = 'Code execution timed out'
    return result


def execute(request):
    if request.method == 'POST':
        lang = request.POST['language']
        question_id = request.POST['id']
        test_id = int(request.POST['currentCase'])
        filename = request.user.username + '.' + lang
        open(filename, 'w').write(request.POST['code'])
        if lang == 'py':
            result = python_execute(question_id, test_id, filename)
        elif lang == 'c':
            result = c_execute(question_id, test_id, filename)
        elif lang == 'java':
            result = java_execute(question_id, test_id, filename)
        os.remove(filename)
        return JsonResponse(result)
