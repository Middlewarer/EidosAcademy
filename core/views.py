from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView, ListView
from courses.models import Course, TopicsBlock, Topic, Content
from users.models import UserProfile

class CoursePageView(DetailView):
    model = Course
    template_name = 'core/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blocks'] = TopicsBlock.objects.filter(course=self.object).order_by('id')
        context['profile'] = UserProfile.objects.get(user=self.request.user)
        return context


class LandingPageView(TemplateView):
    template_name = 'core/landing.html'

class CourseListView(ListView):
    model = Course
    template_name = 'core/course_list_page.html'
    context_object_name = 'courses'


def course_assign_view(request, pk):
    user = request.user
    print(request)
    print(user)
    profile = UserProfile.objects.get(user=user)
    course = Course.objects.get(id=pk)
    profile.course_studied.add(course)
    return HttpResponse(status=204)



