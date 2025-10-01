from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import FormView, TemplateView, DetailView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from PIL import Image
from django.db import transaction
import os

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

class UserPageView(DetailView):
    queryset = UserProfile.objects.select_related("user")  # ВАЖНО: QuerySet, не класс и не экземпляр
    context_object_name = "profile"
    template_name = "users/profile_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.kwargs.get('pk')
        context['courses_studied'] = self.object.course_studied.all()
        return context

    def get_object(self):
        # Берём профиль по user_id из URL
        return get_object_or_404(
            UserProfile.objects.select_related("user").prefetch_related("course_studied"),
            user_id=self.kwargs["pk"],
        )


class UserUpdateView(UpdateView):
    template_name = "users/settings_page.html"
    model = UserProfile
    fields = ['avatar', 'username', 'country_of_origin', 'daily_goal_minutes']

    def get_success_url(self):
        return reverse_lazy('core:landing_page')

    @transaction.atomic
    def form_valid(self, form):
        profile = form.save(commit=False)
        old_path = profile.avatar.path if profile.avatar else None

        resp = super().form_valid(form)

        if 'avatar' in form.changed_data:
            try:
                os.remove(old_path)
            except OSError:
                pass

        print("СОХРАНЯЕМ:", form.cleaned_data)
        return resp

    def form_invalid(self, form):
        print("Ошибки формы:", form.errors)  # логирование для отладки
        return self.render_to_response(self.get_context_data(form=form))






