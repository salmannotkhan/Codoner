from django.urls import path
from .views import index, execute

urlpatterns = [
    path('playground/', index),
    path('execute/', execute),
]
