from django.urls import path
from .views import question_view, signup_view, login_view, logout_view, dashboard_view, add_view, competition_view

urlpatterns = [
    path('', dashboard_view),
    path('login/', login_view, name="login"),
    path('register/', signup_view),
    path('logout/', logout_view),
    path('competition/<id>/', competition_view),
    path('question/<id>/', question_view),
    path('addquestion/', add_view)
]
