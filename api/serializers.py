from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from courses.models import Course
from users.models import UserProfile

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def validate_title(self, value):
        if 'blyat' in value.lower():
            raise serializers.ValidationError('This is insane, youre an idiot')
        return value

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

