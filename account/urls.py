from django.urls import path
from .views import question_view, result_view, signup_view, login_view, logout_view, dashboard_view, competition_view

urlpatterns = [
    path('', dashboard_view),
    path('login/', login_view, name="login"),
    path('register/', signup_view),
    path('logout/', logout_view),
    path('competition/<id>/', competition_view),
    path('competition/<id>/questions/', question_view),
    path('competition/<id>/result/', result_view)
]
