from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework import status

from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import NotAuthenticated

from django.shortcuts import get_object_or_404
from django.db import transaction

from .throttles import LoginRateThrottle

from .throttles import (
    RegisterRateThrottle,
    PasswordRateThrottle,
)


def course_learning_state(course, user):
    progress_by_topic = {
        progress.topic_id: progress.completed
        for progress in UserTopicProgress.objects.filter(
            user=user,
            topic__module__course=course,
        )
    }
    outline = []
    completed_count = 0
    total_count = 0

    for module in course.modules.all().order_by('order', 'id'):
        topic_states = []
        for topic in module.topics.all().order_by('order', 'id'):
            total_count += 1
            if progress_by_topic.get(topic.id) is True:
                status_name = 'completed'
                completed_count += 1
            elif topic.id in progress_by_topic:
                status_name = 'in_progress'
            else:
                status_name = 'not_started'

            topic_states.append({
                'id': topic.id,
                'title': topic.title,
                'order': topic.order,
                'status': status_name,
            })

        if topic_states and all(item['status'] == 'completed' for item in topic_states):
            module_status = 'completed'
        elif any(item['status'] != 'not_started' for item in topic_states):
            module_status = 'in_progress'
        else:
            module_status = 'not_started'

        outline.append({
            'id': module.id,
            'title': module.title,
            'order': module.order,
            'status': module_status,
            'topics': topic_states,
        })

    course_status = (
        'completed' if total_count and completed_count == total_count
        else 'in_progress' if progress_by_topic
        else 'not_started'
    )
    return {
        'status': course_status,
        'completed_topics': completed_count,
        'total_topics': total_count,
        'percent': int(100 * completed_count / total_count) if total_count else 0,
        'modules': outline,
    }



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

            course_progress = None
            if request.user.is_authenticated:
                course_progress = (
                    UserCourseProgress.objects
                    .filter(user=request.user, course=course)
                    .select_related("last_topic__module")
                    .first()
                )
            first_module_id = (
                course.modules.order_by("order", "id")
                .values_list("id", flat=True)
                .first()
            )

            return Response({
                "course_id": course.id,
                "course": serializer.data,
                "is_assigned": course_progress is not None,
                "continue_module_id": (
                    course_progress.last_topic.module_id
                    if course_progress and course_progress.last_topic_id
                    else first_module_id
                ),
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
        course_progress = (
            UserCourseProgress.objects
            .filter(user=request.user, course=module.course)
            .select_related("last_topic__module")
            .first()
        )
        last_topic_id = None
        if (
            course_progress
            and course_progress.last_topic_id
            and course_progress.last_topic.module_id == module.id
        ):
            last_topic_id = course_progress.last_topic_id

        learning_state = course_learning_state(module.course, request.user)
        module_data = dict(serializer.data)
        current_outline = next(
            (item for item in learning_state['modules'] if item['id'] == module.id),
            None,
        )
        if current_outline:
            statuses = {item['id']: item['status'] for item in current_outline['topics']}
            module_data['status'] = current_outline['status']
            module_data['topics'] = [
                {**topic, 'status': statuses.get(topic['id'], 'not_started')}
                for topic in module_data['topics']
            ]

        return Response({
            "module": module_data,
            "last_topic_id": last_topic_id,
            "course_progress": {
                key: learning_state[key]
                for key in ('status', 'completed_topics', 'total_topics', 'percent')
            },
            "course_outline": learning_state['modules'],
        })



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
    throttle_classes = [RegisterRateThrottle]
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
    throttle_classes = [PasswordRateThrottle]

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

        if not created:
            progress.save(update_fields=["last_visited_at"])

        course = progress.topic.module.course
        course_progress, _ = UserCourseProgress.objects.get_or_create(
            user=request.user,
            course=course,
        )
        if course_progress.last_topic_id != progress.topic_id:
            course_progress.last_topic = progress.topic
            course_progress.save(update_fields=["last_topic"])

        return Response(
            {
                'id': progress.id,
                'last_topic': progress.topic_id,
                'status': 'completed' if progress.completed else 'in_progress',
            },
            status=201 if created else 200,
        )


class CompleteTopicView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = TopicVisitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        topic = serializer.validated_data['topic']

        topic_progress, _ = UserTopicProgress.objects.get_or_create(
            user=request.user,
            topic=topic,
        )
        if not topic_progress.completed:
            topic_progress.completed = True
            topic_progress.save(update_fields=['completed', 'last_visited_at'])

        course = topic.module.course
        course_progress, _ = UserCourseProgress.objects.get_or_create(
            user=request.user,
            course=course,
        )
        course_progress.last_topic = topic

        learning_state = course_learning_state(course, request.user)
        course_progress.completed = learning_state['status'] == 'completed'
        course_progress.save(update_fields=['last_topic', 'completed'])

        return Response({
            'topic_id': topic.id,
            'topic_status': 'completed',
            'course_progress': {
                key: learning_state[key]
                for key in ('status', 'completed_topics', 'total_topics', 'percent')
            },
            'course_outline': learning_state['modules'],
        })


class AssignForCourseView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        course = get_object_or_404(
            Course,
            id=request.data.get('course_id'),
            is_published=True,
        )
        progress, created = UserCourseProgress.objects.get_or_create(
            user=request.user,
            course=course,
        )
        response_serializer = UserCourseProgressSerializer(progress)

        return Response(
            {
                "message": "Курс успешно назначен" if created else "Курс уже назначен",
                "data": response_serializer.data
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )








