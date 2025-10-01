from django.db import models
from django.contrib.auth.models import User
from courses.models import Course, Topic
from . import validators
from django.core.validators import FileExtensionValidator
from .validators import validate_image

class UserProfile(models.Model):
    #Initial fields
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    #bio fields
    name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=150, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp']), validate_image])
    name_displayed = models.CharField(max_length=75, null=True, blank=True)

    #Motivational fields
    score = models.PositiveIntegerField(default=0)
    level = models.PositiveSmallIntegerField(default=1)
    streak = models.IntegerField(default=0)
    daily_goal_minutes = models.PositiveIntegerField(default=25)
    daily_goal_score = models.PositiveIntegerField(default=10)

    #Additional information
    localization = models.CharField(max_length=100, null=True, blank=True)
    country_of_origin = models.CharField(max_length=100, null=True, blank=True)
    purpose_language = models.CharField(max_length=100, null=True, blank=True)
    account_created_at = models.DateTimeField(auto_now_add=True)

    #Coursepart
    tasks_confirmed = models.PositiveIntegerField(default=0)
    course_studied = models.ManyToManyField(Course, related_name='students')
    #courses = models.ManyToManyField('courses.Course', related_name='users', blank=True)


    def __str__(self):
        return self.user.username

