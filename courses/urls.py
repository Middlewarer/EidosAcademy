from django.urls import path
from .views import *

urlpatterns = [
    path('courses/<int:pk>/', CoursesApiView.as_view(), name='courses'),
    path('courses/', CoursesApiView.as_view(), name='courses'),
    path('modules/', ModulesApiView.as_view(), name='modules'),
    path('topics/', TopicsApiView.as_view(), name='topics'),
    path('topiclessons/', TopicLessonsApiView.as_view(), name='topic_lessons')
]