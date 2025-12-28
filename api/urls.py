from django.urls import path

from api.views import CourseAPIView

urlpatterns = [
    path('courses/', CourseAPIView.as_view()),
]