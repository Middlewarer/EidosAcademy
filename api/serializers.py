import io

from rest_framework import serializers
from rest_framework.parsers import JSONParser

from django.contrib.auth.models import User

from courses.models import Course, Category, Review
from rest_framework.renderers import JSONRenderer

class ReviewSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    title = serializers.CharField(max_length=255)
    text = serializers.CharField(allow_null=True, required=False, allow_blank=True)
    grade = serializers.DecimalField(max_digits=3, decimal_places=2, min_value=0, max_value=5)
    course = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.grade = validated_data.get('grade', instance.grade)
        instance.save()
        return instance

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'