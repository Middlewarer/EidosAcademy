from rest_framework.serializers import ModelSerializer
from .models import *

class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['title', 'description', 'created_at']


class ModuleSerializer(ModelSerializer):
    class Meta:
        model = Module
        fields = ['title', 'description', 'created_at']


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['title', 'description', 'created_at']


class TopicLessonSerializer(ModelSerializer):
    class Meta:
        model = TopicLesson
        fields = ['content']