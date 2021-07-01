import os
import subprocess

from django.http import JsonResponse
from django.shortcuts import HttpResponse, render

from .models import Question, TestCase


def index(request, id):
    question = Question.objects.get(id=id)
    testcase = TestCase.objects.filter(question=question).first()
    context = {
        'question': question,
        'testcase': testcase
    }
    return render(request, 'playground.html', context=context)


def c_execute(question_id: int, filename: str):
    question = Question.objects.filter(id=question_id).first()
    testcases = TestCase.objects.filter(question=question)
    results = []
    flag = True
    output_file = filename.replace('.c', '.out')
    comp = subprocess.run(['gcc', filename, '-o', output_file],
                          stderr=subprocess.PIPE, text=True)
    if comp.stderr:
        result = {
            'passed': False,
            'error': comp.stderr
        }
        flag = False
        results = [result for i in range(len(testcases))]
        return results, flag
    for testcase in testcases:
        result = {'passed': True}
        code = subprocess.Popen(['./' + output_file], stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            output, error = code.communicate(
                input=testcase.input, timeout=5)
            output = '\r\n'.join(output.splitlines(keepends=False))
            if output != testcase.output:
                result['passed'] = False
                flag = False
                result['error'] = output
        except subprocess.TimeoutExpired:
            result['passed'] = False
            flag = False
            result['error'] = error
        results.append(result)
    os.remove(output_file)
    return results, flag


def java_execute(question_id: int, filename: str):
    # TODO: Fix Class thingy. Not usable right now.
    code_snippet = f'public class {filename.replace(".java", "")} {{{open(filename, "r").read()}}}'
    open(filename, 'w').write(code_snippet)
    output_file = filename.replace('.java', '')

    question = Question.objects.filter(id=question_id).first()
    testcases = TestCase.objects.filter(question=question)
    results = []
    flag = True
    comp = subprocess.run(['javac', filename],
                          stderr=subprocess.PIPE, text=True)
    if comp.stderr:
        result = {
            'passed': False,
            'error': comp.stderr
        }
        flag = False
        results = [result for i in range(len(testcases))]
        return results, flag
    for testcase in testcases:
        result = {'passed': True}
        code = subprocess.Popen(['java',  output_file], stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            output, error = code.communicate(
                input=testcase.input, timeout=5)
            output = '\r\n'.join(output.splitlines(keepends=False))
            if output != testcase.output:
                result['passed'] = False
                flag = False
                result['error'] = output
        except subprocess.TimeoutExpired:
            result['passed'] = False
            flag = False
            result['error'] = error
        results.append(result)
    os.remove(output_file + '.class')
    return results, flag


def python_execute(question_id: int, filename: str):
    question = Question.objects.filter(id=question_id).first()
    testcases = TestCase.objects.filter(question=question)
    results = []
    flag = True
    for testcase in testcases:
        code = subprocess.Popen(['python3', filename], stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        result = {'passed': True}
        try:
            output, error = code.communicate(input=testcase.input, timeout=5)
            output = '\r\n'.join(output.splitlines(keepends=False))
            if output != testcase.output:
                result['passed'] = False
                flag = False
                result['error'] = output
        except subprocess.TimeoutExpired:
            result['passed'] = False
            flag = False
            result['error'] = error
        results.append(result)
    return results, flag


def execute(request):
    if request.method == 'POST':
        lang = request.POST['language']
        question_id = request.POST['id']
        filename = 'somethingwirld.' + lang
        open(filename, 'w').write(request.POST['code'])
        if lang == 'py':
            results, flag = python_execute(question_id, filename)
        elif lang == 'c':
            results, flag = c_execute(question_id, filename)
        elif lang == 'java':
            results, flag = java_execute(question_id, filename)
        os.remove(filename)
        return JsonResponse({
            'success': flag,
            'output': results,
        })
