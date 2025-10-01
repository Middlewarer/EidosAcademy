from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('course/<int:pk>/', views.CoursePageView.as_view(), name='course_detail'),
    path('course/<int:pk>/enroll/', views.course_assign_view, name='course_assign'),
    path('', views.LandingPageView.as_view(), name='landing_page'),
    path('course_list/', views.CourseListView.as_view(), name='course_list'),
    path('topic/<int:topic_id>/', views.TopicStepView.as_view(), name='topic_detail'),
    path('content/<int:pk>/', views.LessonPageView.as_view(), name='lesson_page'),
    path('content/<int:pk>/finished', views.topic_finished_button, name='topic_finished'),
]