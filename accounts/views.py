from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.views.generic import CreateView, DetailView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from .forms import SignupForm

User = get_user_model()
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignupForm, UserUpdateForm

class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Autologin after signup
        login(self.request, self.object)
        return response

class ProfileView(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Real statistics for questions and answers
        context['questions_count'] = self.request.user.questions.count()
        context['answers_count'] = self.request.user.answers.count()
        return context

@login_required
def logout_user(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')

class PasswordChangeManualView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_url = reverse_lazy('password_change_done')

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user
