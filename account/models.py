from django.db import models
from django.contrib.auth.models import User
from main.models import Competition


class Detail(models.Model):
    id = models.OneToOneField(
        to=User, on_delete=models.CASCADE, primary_key=True)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
