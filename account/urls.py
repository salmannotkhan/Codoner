from django.urls import path
from .views import signup_view, login_view, logout_view, dashboard_view, add_view

urlpatterns = [
    path('register/', signup_view),
    path('login/', login_view, name="login"),
    path('logout/', logout_view),
    path('', dashboard_view),
    path('addquestion/', add_view)
]
