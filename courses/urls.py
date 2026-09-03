from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)


router = DefaultRouter()
router.register("modules", ModulesViewSet, basename="modules")

urlpatterns = [
    path('courses/<int:pk>/', CoursesApiView.as_view(), name='courses'),
    path('courses/', CoursesApiView.as_view(), name='courses'),
    path('topics/', TopicsApiView.as_view(), name='topics'),
    path('topiclessons/', TopicLessonsApiView.as_view(), name='topic_lessons'),
    path('modules/<int:pk>/', ModuleDetailApiView.as_view()),

    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path('register/', RegisterUserApiView.as_view(), name='register'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('complete/', UserTopicProgressView.as_view(), name='progress_complete'),
]

urlpatterns += router.urls