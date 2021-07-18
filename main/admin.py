from django.contrib import admin
from .models import Competition, Question, Result, TestCase

admin.site.register(Competition)
admin.site.register(Question)
admin.site.register(TestCase)
admin.site.register(Result)
