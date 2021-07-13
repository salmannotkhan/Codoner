from django.db import models
from django.contrib.auth.models import User


class Details(models.Model):
    id = models.OneToOneField(
        to=User, on_delete=models.CASCADE, primary_key=True)
    competition_name = models.CharField(max_length=256)
