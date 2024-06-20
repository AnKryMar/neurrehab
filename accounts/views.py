# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views import View
from .forms import PatientRegistrationForm, SpecialistRegistrationForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth import logout

class RegisterView(View):
    def get(self, request):
        patient_form = PatientRegistrationForm()
        specialist_form = SpecialistRegistrationForm()
        return render(request, 'accounts/register.html',
                      {'patient_form': patient_form, 'specialist_form': specialist_form})

    def post(self, request):
        if 'patient' in request.POST:
            form = PatientRegistrationForm(request.POST)
        else:
            form = SpecialistRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'patient' if isinstance(form, PatientRegistrationForm) else 'specialist'
            user.save()
            login(request, user)
            return redirect('profile')
        patient_form = PatientRegistrationForm() if isinstance(form, SpecialistRegistrationForm) else form
        specialist_form = SpecialistRegistrationForm() if isinstance(form, PatientRegistrationForm) else form
        return render(request, 'accounts/register.html',
                      {'patient_form': patient_form, 'specialist_form': specialist_form})


class ProfileView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = ProfileUpdateForm(instance=request.user)
        return render(request, 'accounts/profile.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, 'accounts/profile.html', {'form': form})


class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')  # Перенаправление после выхода
