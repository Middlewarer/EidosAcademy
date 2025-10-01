from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

from articles.models import Article


class MainArticlePageView(ListView):
    template_name = 'articles/main_article_page.html'
    model = Article
    context_object_name = 'articles'


class ArticleDetailView(DetailView):
    template_name = 'articles/article_detail.html'
    model = Article
    context_object_name = 'article'

