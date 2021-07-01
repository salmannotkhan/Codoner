from django.urls import path
from .views import index, execute

urlpatterns = [
    path('playground/<id>', index),
    path('execute/', execute),
]
