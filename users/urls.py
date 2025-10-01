from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'users'

urlpatterns = [
    path('login/', views.LoginPageView.as_view(), name='user_login'),
    path('register/', views.RegisterPageView.as_view(), name='user_register'),
    path('profile/<int:pk>/', views.UserPageView.as_view(), name='profile_page'),
    path('profile/<int:pk>/settings/', views.UserUpdateView.as_view(), name='settings_page'),
]

