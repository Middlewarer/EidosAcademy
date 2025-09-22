from django.urls import path
from . import views

urlpatterns = [
    path('course/', views.CoursePageView.as_view(), name='course_detail'),
    path('landing/', views.LandingPageView.as_view(), name='landing'),
    path('course_list/', views.CourseListView.as_view(), name='course_list'),
]