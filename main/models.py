from django.db import models
from django.contrib.auth.models import User


class Competition(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    input = models.CharField(max_length=256)
    output = models.TextField()

    def __str__(self):
        return f'{self.question}({self.input})'


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    testcase = models.CharField(max_length=256)
    lang = models.CharField(max_length=256, blank=True)
    code = models.TextField()
    passed = models.BooleanField()
