from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy

from .forms import LoginForm, RegisterForm
from django.contrib.auth.models import User



class LoginPageView(FormView):
    form_class = LoginForm
    template_name = 'users/sign_in.html'
    success_url = reverse_lazy('course_detail')

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
    success_url = reverse_lazy('course_detail')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class UserPageView(TemplateView):
    template_name = 'users/profile_page.html'



