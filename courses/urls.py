from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("modules", ModulesViewSet, basename="modules")

urlpatterns = [
    path('courses/<int:pk>/', CoursesApiView.as_view(), name='courses'),
    path('courses/', CoursesApiView.as_view(), name='courses'),
    path('topics/', TopicsApiView.as_view(), name='topics'),
    path('topiclessons/', TopicLessonsApiView.as_view(), name='topic_lessons'),
    path('modules/<int:pk>/', ModuleDetailApiView.as_view())
]

urlpatterns += router.urls