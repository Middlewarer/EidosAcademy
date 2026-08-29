from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404



class CoursesApiView(APIView):
    def get(self, request, pk=None):
        if pk:
            course = get_object_or_404(Course, id=pk)
            serializer = CourseDetailSerializer(course)
            module_counter = course.modules.count()
            topic_counter = Topic.objects.filter(module__course=course).count()
            topics = Topic.objects.filter(module__course=course).order_by("module__order", "order")
            topic_serializer = TopicSerializer(many=True, instance=topics)

            return Response({
                "course": serializer.data,
                "module_counter": module_counter,
                "topic_counter": topic_counter,
                "topics": topic_serializer.data,
            })
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


class RegisterUserApiView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=reqeust.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User Created"
            }, status=status.HTTP_201_CREATED)

        return Response({'error': "Chtoto ne tak"}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]  # только для авторизованных

    def get(self, request):
        user = request.user

        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })




