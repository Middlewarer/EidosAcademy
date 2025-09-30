from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainArticlePageView.as_view(), name='main_article'),
]