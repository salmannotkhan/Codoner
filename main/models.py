from django.db import models


class Question(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField()
    # competition = models.ForeignKey(Competition, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class TestCase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    input = models.CharField(max_length=256)
    output = models.TextField()

    def __str__(self):
        return f'{self.question}({self.input})'
