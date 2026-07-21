from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import *


        
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
        fields = ['title', 'short_description', 'description', 'created_at']


class CourseDetailSerializer(ModelSerializer):
    modules = ModuleSerializer(read_only=True, many=True)
    class Meta:
        model = Course
        fields = ['title', 'short_description', 'created_at', 'modules']





