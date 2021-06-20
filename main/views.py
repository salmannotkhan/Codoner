from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import subprocess
import os


def index(request):
    return render(request, 'playground.html')


def c_execute(filename: str):
    output_file = filename.replace('.c', '.out')
    comp = subprocess.run(['gcc', filename, '-o', output_file],
                          stderr=subprocess.PIPE, text=True)
    output = ""
    if comp.stderr:
        error = comp.stderr
    else:
        code = subprocess.Popen(['./' + output_file], stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            output, error = code.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            code.kill()
            error = 'Code execution timed out'
        os.remove(output_file)
    return output, error


def java_execute(filename: str):
    code_snippet = f'public class {filename.replace(".java", "")} {{{open(filename, "r").read()}}}'
    open(filename, 'w').write(code_snippet)
    output_file = filename.replace('.java', '')
    comp = subprocess.run(['javac', filename],
                          stderr=subprocess.PIPE, text=True)
    output = ''
    if comp.stderr:
        error = comp.stderr
    else:
        code = subprocess.Popen(['java',  output_file], stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        try:
            output, error = code.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            code.kill()
            error = 'Code execution timed out'
        os.remove(output_file + '.class')
    return output, error


def python_execute(filename):
    code = subprocess.Popen(['python3', filename], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = ''
    try:
        output, error = code.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        error = 'Code execution timed out'
    return output, error


def execute(request):
    if request.method == 'POST':
        lang = request.POST['language']
        filename = 'somethingwirld.' + lang
        open(filename, 'w').write(request.POST['code'])
        if lang == 'py':
            output, error = python_execute(filename)
        elif lang == 'c':
            output, error = c_execute(filename)
        elif lang == 'java':
            output, error = java_execute(filename)

        os.remove(filename)
        if error:
            return JsonResponse({
                'error': True,
                'details': error
            })
        return JsonResponse({
            'error': False,
            'output': output
        })
