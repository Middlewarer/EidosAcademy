from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from courses.models import Course
from .serializers import CourseSerializer, UserProfileSerializer
from users.models import UserProfile


#----------CreateApis

class CreateCourseApi(CreateAPIView):
    model = Course
    serializer_class = CourseSerializer

class CreateProfileApi(CreateAPIView):
    model = UserProfile
    serializer_class = UserProfileSerializer

#----------ListApis

class ListCoursesApi(ListAPIView):
    model = Course
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class ListUsersApi(ListAPIView):
    model = UserProfile
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()








