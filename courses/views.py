from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *


class CoursesApiView(APIView):
    def get(self, request):
        queryset = Course.objects.all()
        serializer = CourseSerializer(many=True, instance=queryset)

        return Response({'courses': serializer.data})


class ModulesApiView(generics.GenericAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'modules': serializer.data})


class TopicsApiView(APIView):
    def get(self, reqeust):
        queryset = Topic.objects.all()
        serializer = TopicSerializer(many=True, instance=queryset)

        return Response({'topics': serializer.data})

class TopicLessonsApiView(APIView):
    def get(self, reqeust):
        queryset = TopicLesson.objects.all()
        serializer = TopicLessonSerializer(many=True, instance=queryset)

        return Response({'topics': serializer.data,
                         'count': queryset.count()})




