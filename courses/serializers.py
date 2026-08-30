from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.db.models import Q

from .models import *

from django.contrib.auth.models import User


        
class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'description', 'created_at']

class ModuleSerializer(ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = [
            "id",
            "title",
            "description",
            "topics",
        ]


class TopicLessonSerializer(ModelSerializer):
    class Meta:
        model = TopicLesson
        fields = ['content']

class TopicDetailSerializer(ModelSerializer):
    lessons = TopicLessonSerializer(
        source='topiclesson_set',
        many=True,
        read_only=True
    )
    class Meta:
        model = Topic
        fields = ['id', 'title', 'description', 'order', 'lessons']

class ModuleDetailSerializer(ModelSerializer):
    topics = TopicDetailSerializer(many=True, read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'course_title', 'topics']


class CourseListSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'short_description', 'description', 'created_at']


class CourseDetailSerializer(ModelSerializer):
    modules = ModuleSerializer(read_only=True, many=True)
    class Meta:
        model = Course
        fields = ['title', 'short_description', 'created_at', 'modules']

class UserModuleProgressSerializer(ModelSerializer):
    class Meta:
        model = UserModuleProgress
        fields = '__all__'

class UserTopicProgressSerializer(ModelSerializer):
    class Meta:
        model = UserTopicProgress
        fields = '__all__'


class AchievmentSerializer(ModelSerializer):
    class Meta:
        model = Achievment
        fields = ['title', 'icon', 'small_description']


class RandomCourseSerializer(ModelSerializer):
    progress_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'title', 'short_description', 'category',
            'image', 'difficulty', 'total_lessons', 'progress_status']

        


class UserSerializer(ModelSerializer):
    courses_count = serializers.SerializerMethodField()
    topics_count = serializers.SerializerMethodField()
    achievments = AchievmentSerializer(many=True, read_only=True)
    random_course = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', \
        'date_joined', 'courses_count', 'topics_count', 'achievments', 'random_course']

    def get_random_course(self, obj):
        import random
        random_id = random.choice(UserCourseProgress.objects.filter(user=obj).values_list('id', flat=True))

        try:
            course = Course.objects.get(id=random_id)
            total_topics = Topic.objects.filter(module__course=course).count()
            completed_topics = UserTopicProgress.objects.filter(
                user=obj,
                topic__module__course=course.id,
                completed=True
            ).count() 

            return {
                'id': course.id,
                'title': course.title,
                'short_description': course.short_description,
                'category': course.category.title,
                'progress': int(100 / total_topics * completed_topics)
            }

        except Course.DoesNotExist:
            return None
        return random_id
        

    def get_courses_count(self, obj):
        return UserCourseProgress.objects.filter(user=obj).count()

    def get_topics_count(self, obj):
        topics_count = UserTopicProgress.objects.filter(user=obj).count()
        return topics_count




class UserRegistrationSerializer(ModelSerializer):
    password2 = serializers.CharField(style={'input_type': "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Sorry, incorrect"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )

        return user




