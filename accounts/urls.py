# accounts/urls.py
from django.urls import path
from .views import RegisterView, ProfileView, CustomLogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),
]