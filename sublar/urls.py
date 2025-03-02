"""
URL configuration for sublar project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from accounts.views import dashboard_view, user_login, register_view, referral_register, activate, team_view, home_redirect


# 📌 Функция для редиректа неавторизованных пользователей на login
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect("dashboard")  # Если авторизован, на дашборд
    return redirect("login")  # Если не авторизован, на логин


urlpatterns = [
    path("ref/<str:referral_code>/", referral_register, name="referral_register"),
    path("", home_redirect, name="home"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("login/", user_login, name="login"),
    path("register/", register_view, name="register"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("team/", team_view, name="team"),
]
