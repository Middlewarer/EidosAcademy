from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    #Initial fields
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    #bio fields
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=150)
    avatar = models.ImageField(upload_to='avatars/')
    name_displayed = models.CharField(max_length=75)

    #Motivational fields
    score = models.PositiveIntegerField(default=0)
    level = models.PositiveSmallIntegerField(default=1)
    streak = models.IntegerField(default=0)
    daily_goal_minutes = models.PositiveIntegerField(default=25)
    daily_goal_score = models.PositiveIntegerField(default=10)

    #Additional information
    localization = models.CharField(max_length=100)
    country_of_origin = models.CharField(max_length=100)
    purpose_language = models.CharField(max_length=100)
    account_created_at = models.DateTimeField(auto_now=True)

    #Coursepart
    #courses = models.ManyToManyField('courses.Course', related_name='users', blank=True)

    def __str__(self):
        return self.name_displayed

