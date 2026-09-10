from django.urls import path
from .views import *
from .auth_views import LoginView, RefreshView, LogoutView



urlpatterns = [
    path('courses/<int:pk>/', CoursesApiView.as_view(), name='courses'),
    path('courses/', CoursesApiView.as_view(), name='courses'),
    path('topics/', TopicsApiView.as_view(), name='topics'),
    path('topiclessons/', TopicLessonsApiView.as_view(), name='topic_lessons'),
    path('modules/<int:pk>/', ModuleDetailApiView.as_view()),
    path('modules/', ModulesApiView.as_view(), name='modules'),

    path("token/", LoginView.as_view()),
    path("token/refresh/", RefreshView.as_view()),
    path("logout/", LogoutView.as_view()),
    path('register/', RegisterUserApiView.as_view(), name='register'),
    path('me/', CurrentUserView.as_view(), name='me'),
    path('me/password/', ChangePasswordView.as_view(), name='change_password'),
    path('complete/', UserTopicProgressView.as_view(), name='progress_complete'),
    path('progress/visit/', UserTopicProgressView.as_view(), name='progress_visit'),
    path('progress/complete/', CompleteTopicView.as_view(), name='progress_complete_topic'),
    path("assign/", AssignForCourseView.as_view(), name="assign_course"),
    path("feedback/", FeedbackView.as_view(), name="feedback"),
]

