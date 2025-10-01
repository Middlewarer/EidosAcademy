from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.MainArticlePageView.as_view(), name='main_article'),
    path('<int:pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
]