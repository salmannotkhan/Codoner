from django.urls import path
from .views import index, playground, execute

urlpatterns = [
    path('', index),
    path('playground/<id>', playground),
    path('execute/', execute),
]
