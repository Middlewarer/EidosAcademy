from django.urls import path
from . import views

urlpatterns = [
    path('create_course/', views.CreateCourseApi.as_view(), name='create_api'),
    path('list_courses/', views.ListCoursesApi.as_view(), name='list_courses_api'),
    path('list_users/', views.ListUsersApi.as_view(), name='list_users_api'),
    path('create_user/', views.CreateProfileApi.as_view(), name='create_profile_api'),
               ]