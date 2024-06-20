# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class PatientRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'email': _('Электронная почта'),
            'password1': _('Пароль'),
            'password2': _('Подтверждение пароля'),
        }


class SpecialistRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'middle_name', 'email', 'phone_number', 'specialization', 'experience', 'password1', 'password2')
        labels = {
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'middle_name': _('Отчество'),
            'email': _('Электронная почта'),
            'phone_number': _('Телефон'),
            'specialization': _('Специализация'),
            'experience': _('Опыт'),
            'password1': _('Пароль'),
            'password2': _('Подтверждение пароля'),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'middle_name', 'birth_date', 'phone_number', 'country', 'city', 'avatar')
        widgets = {
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'middle_name': _('Отчество'),
            'birth_date': _('Дата рождения'),
            'phone_number': _('Телефон'),
            'country': _('Страна'),
            'city': _('Город'),
            'avatar': _('Аватар'),
            'email_notifications': _('Email уведомления'),
            'sms_notifications': _('SMS уведомления'),
        }