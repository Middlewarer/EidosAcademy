from django.shortcuts import render
from rest_framework import generics
from courses.models import Course
from .serializers import CourseListSerializer


class CourseAPIView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer