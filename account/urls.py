from django.urls import path
from .views import participants_download_view, question_view, result_download_view, result_view, signup_view, login_view, logout_view, dashboard_view, competition_view, detailed_result_view

urlpatterns = [
    path('', dashboard_view),
    path('login/', login_view, name="login"),
    path('register/', signup_view),
    path('logout/', logout_view),
    path('competition/<id>/', competition_view),
    path('question/<id>/', question_view),
    path('download/participants/<id>', participants_download_view),
    path('download/result/<id>', result_download_view),
    path('competition/<id>/result/', result_view),
    path('competition/<cid>/result/<uid>/', detailed_result_view)
]
