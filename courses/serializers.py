from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

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

class UserProgressSerializer(ModelSerializer):
    class Meta:
        model = UserProgress
        fields = '__all__'


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




