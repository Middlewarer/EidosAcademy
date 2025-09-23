from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView, TemplateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from .models import UserProfile



class LoginPageView(FormView):
    form_class = LoginForm
    template_name = 'users/sign_in.html'
    success_url = reverse_lazy('core:landing_page')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Неправильные данные')
            return self.form_invalid(form)


class RegisterPageView(FormView):
    form_class = RegisterForm
    template_name = 'users/sign_up.html'
    success_url = reverse_lazy('core:landing_page')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class UserPageView(LoginRequiredMixin, DetailView):
    template_name = 'users/profile_page.html'
    model = UserProfile
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context

    def get_queryset(self):
        return self.request.user.profile



