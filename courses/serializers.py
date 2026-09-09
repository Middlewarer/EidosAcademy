from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.db.models import Q

from .models import *

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError


        
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
    next_module_id = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'order', 'course_title', 'topics', 'next_module_id']

    def get_next_module_id(self, obj):
        obj_id = (
            Module.objects
            .filter(course=obj.course, order__gt=obj.order)
            .order_by('order', 'id')
            .values_list('id', flat=True)
            .first()
        )
        return obj_id



class CourseListSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'short_description', 'description', 'created_at']


class CourseDetailSerializer(ModelSerializer):
    modules = ModuleSerializer(read_only=True, many=True)
    class Meta:
        model = Course
        fields = ['title', 'short_description', 'created_at', 'modules']

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


class TopicVisitSerializer(serializers.Serializer):
    topic = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.filter(module__course__is_published=True)
    )

    


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
        progress = (
            UserCourseProgress.objects
            .filter(user=obj, course__is_published=True)
            .select_related("course__category", "last_topic__module")
            .order_by("-assigned_at", "-id")
            .first()
        )
        if not progress:
            return None

        course = progress.course
        total_topics = Topic.objects.filter(module__course=course).count()
        completed_topics = UserTopicProgress.objects.filter(
            user=obj,
            topic__module__course=course,
            completed=True,
        ).count()
        first_module_id = (
            Module.objects.filter(course=course)
            .order_by("order", "id")
            .values_list("id", flat=True)
            .first()
        )

        return {
            'id': course.id,
            'title': course.title,
            'short_description': course.short_description,
            'category': course.category.title,
            'progress': int(100 * completed_topics / total_topics) if total_topics else 0,
            'continue_module_id': (
                progress.last_topic.module_id if progress.last_topic_id else first_module_id
            ),
        }
        

    def get_courses_count(self, obj):
        return UserCourseProgress.objects.filter(user=obj).count()

    def get_topics_count(self, obj):
        topics_count = UserTopicProgress.objects.filter(user=obj, completed=True).count()
        return topics_count




class UserRegistrationSerializer(ModelSerializer):
    password2 = serializers.CharField(style={'input_type': "password"}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})

        try:
            validate_password(attrs['password'], user=User(username=attrs['username']))
        except DjangoValidationError as error:
            raise serializers.ValidationError({'password': error.messages})

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True, trim_whitespace=False)
    new_password = serializers.CharField(write_only=True, trim_whitespace=False)
    confirm_password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['current_password']):
            raise serializers.ValidationError({'current_password': 'Текущий пароль неверен.'})
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'confirm_password': 'Пароли не совпадают.'})
        if attrs['new_password'] == attrs['current_password']:
            raise serializers.ValidationError({'new_password': 'Новый пароль должен отличаться от текущего.'})
        try:
            validate_password(attrs['new_password'], user=user)
        except DjangoValidationError as error:
            raise serializers.ValidationError({'new_password': error.messages})
        return attrs

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save(update_fields=['password'])
        return instance


class UserCourseProgressSerializer(ModelSerializer):
    class Meta:
        model = UserCourseProgress
        fields = ['id', 'course', 'completed', 'assigned_at', 'last_topic']
        read_only_fields = fields


class FeedbackSerializer(ModelSerializer):
    author = serializers.SerializerMethodField()
    kind_label = serializers.CharField(source='get_kind_display', read_only=True)
    status_label = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Feedback
        fields = [
            'id', 'kind', 'kind_label', 'status', 'status_label',
            'author', 'message', 'created_at',
        ]

    def get_author(self, obj):
        return obj.name or (obj.user.get_full_name() if obj.user else '') or 'Аноним'


class CreateFeedbackSerializer(ModelSerializer):
    website = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Feedback
        fields = ['kind', 'name', 'contact', 'message', 'page_url', 'website']

    def validate(self, attrs):
        if attrs.pop('website', ''):
            raise serializers.ValidationError({'message': 'Не удалось отправить сообщение.'})
        attrs['name'] = attrs.get('name', '').strip()
        attrs['message'] = attrs['message'].strip()
        if len(attrs['message']) < 10:
            raise serializers.ValidationError({'message': 'Напишите хотя бы 10 символов.'})
        return attrs

