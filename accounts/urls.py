from django.urls import path
from .views import register_view, user_login, dashboard_view, activate
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]