from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *

from django.shortcuts import get_object_or_404



class CoursesApiView(APIView):
    def get(self, request, pk=None):
        if pk:
            course = Course.objects.get(id=pk)
            serializer = CourseDetailSerializer(course)
            module_counter = course.modules.count()
            topic_counter = Topic.objects.filter(module__course=course).count()
            topics = Topic.objects.filter(module__course=course).order_by("module__order", "order")
            topic_serializer = TopicSerializer(many=True, instance=topics)

            return Response({"course": serializer.data,
                            "module_counter": module_counter,
                            "topic_counter": topic_counter,
                            "topics": topic_serializer.data})
        else:
            queryset = Course.objects.all()
            serializer = CourseListSerializer(queryset, many=True)
            return Response({'courses': serializer.data})



class ModulesViewSet(ModelViewSet):
    serializer_class = ModuleSerializer
    queryset = Module.objects.all()


class ModuleDetailApiView(APIView):
    def get(self, request, pk):
        module = get_object_or_404(Module, id=pk)
        serializer = ModuleDetailSerializer(module)
        return Response({"module": serializer.data})



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




