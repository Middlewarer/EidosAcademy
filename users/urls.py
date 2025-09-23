from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginPageView.as_view(), name='user_login'),
    path('register/', views.RegisterPageView.as_view(), name='user_register'),
    path('profile/<int:pk>/', views.UserPageView.as_view(), name='profile_page'),
]