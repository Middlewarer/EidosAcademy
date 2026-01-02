from django.shortcuts import render, get_object_or_404
from rest_framework import generics, views, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from users.models import UserProfile
from .serializers import CourseSerializer, ReviewSerializer

from courses.models import Course
from django.contrib.auth.models import User

class CourseCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(data={"Вы отправили GET-запрос": "Так что все ок"}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CourseCreationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = serializer.save(author=self.request.user)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ReviewCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_pk):

        user = UserProfile.objects.get(user=self.request.user)
        course = get_object_or_404(Course, pk=course_pk)

        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review = serializer.save(user=user, course=course)


        return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)


class CourseApiViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer




