from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    user = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=255)
    text = models.TextField(blank=True, null=True)
    grade = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)])
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        unique_together = [('user', 'course')]


class Category(models.Model):
    title = models.CharField(max_length=100)


class Course(models.Model):
    title = models.CharField(max_length=255)
    main_image = models.ImageField(upload_to='courses/', null=True, blank=True)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='courses', null=True, blank=True)

    def __str__(self):
        return self.title


    def __str__(self):
        return self.title

class TopicsBlock(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name='blocks')

    def __str__(self):
        return self.title

class Topic(models.Model):
    block = models.ForeignKey(TopicsBlock, on_delete=models.CASCADE, null=True, blank=True, related_name='topics')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    min_time_duration = models.IntegerField(default=1)


    def __str__(self):
        return self.title

class UserTopicProgress(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    topic_id = models.ForeignKey(Topic, on_delete=models.CASCADE)
    percentage = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    started_at = models.DateTimeField(auto_now=True)
    finished_at = models.DateTimeField(null=True, blank=True)


class Content(models.Model):
    class Type(models.TextChoices):
        VIDEO = 'video', 'Видео'
        TASK = "task", "Задание"
        TEXT = "text", "Текст"
        QUIZ = "quiz", "Тест"

    topic = models.ForeignKey(Topic, on_delete=models.PROTECT)
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.TEXT)
    title = models.CharField(max_length=255)
    video_url = models.URLField(blank=True, null=True)
    video_duration = models.PositiveIntegerField(blank=True, null=True)
    essence_html = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.topic.title} | {self.title}'


