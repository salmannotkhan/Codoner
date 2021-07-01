from django.urls import path
from .views import signup_view, login_view, logout_view, dashboard_view, add_view

urlpatterns = [
    path('', dashboard_view),
    path('login/', login_view, name="login"),
    path('register/', signup_view),
    path('logout/', logout_view),
    path('addquestion/', add_view)
]
