from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import NotAuthenticated

from django.shortcuts import get_object_or_404



class CoursesApiView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, pk=None):
        if pk:
            course = get_object_or_404(Course, id=pk)
            if not course.is_published:
                return Response({"message": "Sorry, course was not published yet!"}, status=status.HTTP_404_NOT_FOUND)

            
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
            queryset = Course.objects.filter(is_published=True)
            serializer = CourseListSerializer(queryset, many=True)
            return Response({'courses': serializer.data})


class ModulesApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Module.objects.filter(course__is_published=True)
        return Response(ModuleSerializer(queryset, many=True).data)


class ModuleDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        module = get_object_or_404(Module, id=pk)

        if not module.course.is_published:
            return Response({"message": "Sorry, course was not published yet!"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ModuleDetailSerializer(module)
        return Response({"module": serializer.data})



class TopicsApiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        queryset = Topic.objects.filter(module__course__is_published=True)
        serializer = TopicSerializer(many=True, instance=queryset)

        return Response({'topics': serializer.data})

class TopicLessonsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = TopicLesson.objects.filter(parent_topic__module__course__is_published=True)
        serializer = TopicLessonSerializer(many=True, instance=queryset)

        return Response({'topics': serializer.data,
                         'count': queryset.count()})


class RegisterUserApiView(APIView):
    permission_classes = [NotAuthenticated]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "User Created"
            }, status=status.HTTP_201_CREATED)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UpdateUserSerializer(data=request.data, instance=request.user, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(UserSerializer(request.user).data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            instance=request.user, data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Пароль обновлён.'})


class UserTopicProgressView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TopicVisitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        progress, created = UserTopicProgress.objects.get_or_create(
            user=request.user,
            topic=serializer.validated_data['topic'],
        )

        return Response(
            {'id': progress.id},
            status=201 if created else 200,
        )








