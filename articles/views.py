from django.shortcuts import render
from django.views.generic import TemplateView


class MainArticlePageView(TemplateView):
    template_name = 'articles/main_article_page.html'

