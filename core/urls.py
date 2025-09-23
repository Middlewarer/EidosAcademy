from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('course/<int:pk>/', views.CoursePageView.as_view(), name='course_detail'),
        path('course/<int:pk>/enroll/', views.course_assign_view, name='course_assign'),
    path('landing/', views.LandingPageView.as_view(), name='landing_page'),
    path('course_list/', views.CourseListView.as_view(), name='course_list'),
    
]