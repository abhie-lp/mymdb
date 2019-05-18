from . import views
from django.urls import path
from django.contrib.auth import views as auth_view

app_name = "user"

urlpatterns = [
    path("login/", auth_view.LoginView.as_view(template_name="user/login.html"), name="login"),
    path("logout/", auth_view.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
]
