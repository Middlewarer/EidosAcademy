import datetime

from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import DetailView, TemplateView, ListView

from articles.models import Article
from courses.models import Course, TopicsBlock, Topic, Content, UserTopicProgress
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        courses = Course.objects.order_by('id')[:3]
        context['courses'] = courses
        context['articles'] = Article.objects.order_by('id')[:3]
        return context


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
    return redirect(request.META.get('HTTP_REFERER', '/'))


class TopicStepView(DetailView):
    model = Topic
    template_name = 'core/topic_steps.html'

    def get_object(self):
        self.object = Topic.objects.get(id=self.kwargs['topic_id'])
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['contents'] = Content.objects.filter(topic=self.object)
        return context


class LessonPageView(UserPassesTestMixin, DetailView):
    model = Content
    template_name = 'core/lesson.html'
    context_object_name = 'content'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.object.topic.block.course

        # проверяем прогресс
        user_prog, _ = UserTopicProgress.objects.get_or_create(user=self.request.user)
        is_finished = user_prog.finished_contents.filter(id=self.object.id).exists()

        context['course'] = course
        context['is_finished'] = is_finished
        return context

    def test_func(self):
        self.course = self.get_object().topic.block.course
        user = UserProfile.objects.get(user=self.request.user)
        return self.course not in user.course_studied.all()

    def handle_no_permission(self):
        return redirect('core:course_detail', pk=self.course.pk)


def topic_finished_button(request, pk):
    content = get_object_or_404(Content, pk=pk)
    topic = content.topic
    user_prog, _ = UserTopicProgress.objects.get_or_create(user=request.user)
    user_prog.finished_contents.add(content)
    return redirect('core:topic_detail', topic_id=topic.id)







