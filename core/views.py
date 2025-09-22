from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from courses.models import Course

class CoursePageView(ListView):
    model = Course
    template_name = 'core/course_detail.html'

class LandingPageView(TemplateView):
    template_name = 'core/landing.html'

class CourseListView(ListView):
    model = Course
    template_name = 'core/course_list_page.html'